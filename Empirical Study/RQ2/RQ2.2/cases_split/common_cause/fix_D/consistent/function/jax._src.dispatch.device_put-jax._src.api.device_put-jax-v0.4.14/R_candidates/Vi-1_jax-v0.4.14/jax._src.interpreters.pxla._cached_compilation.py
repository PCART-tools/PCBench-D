@weakref_lru_cache
def _cached_compilation(computation, name, mesh, spmd_lowering,
                        tuple_args, auto_spmd_lowering,
                        _allow_propagation_to_outputs, host_callbacks, backend,
                        da, pmap_nreps, compiler_options_keys,
                        compiler_options_values):
  device_assignment = da.device_assignment if isinstance(
      da, _DeviceAssignment) else da

  # TODO(phawkins): One would normally just write:
  # dev = np.array(device_assignment)
  # The formulation below is substantially faster if there are many devices.
  # If we were to optimize __getattr__ on xc.Device we might not need this
  # workaround.
  dev = np.vectorize(lambda i: device_assignment[i], otypes=[object])(
    np.arange(len(device_assignment))
  )
  if pmap_nreps > 1:
    num_replicas, num_partitions = pmap_nreps, 1
  elif spmd_lowering:
    num_replicas, num_partitions = 1, dev.size
  else:
    num_replicas, num_partitions = dev.size, 1

  if pmap_nreps > 1:
    # In `jit` device_assignment is set to None when num_replicas > 1. Do
    # the same thing here too.
    xla_device_assignment = None
  else:
    xla_device_assignment = dev.reshape((num_replicas, num_partitions))

  if compiler_options_keys is None:
    compiler_options = None
  else:
    compiler_options = dict(safe_zip(compiler_options_keys, compiler_options_values))

  fdo_profile = (None if compiler_options is None else
                 compiler_options.pop("fdo_profile", None))

  compile_options = xb.get_compile_options(
      num_replicas=num_replicas,
      num_partitions=num_partitions,
      device_assignment=xla_device_assignment,
      use_spmd_partitioning=spmd_lowering,
      use_auto_spmd_partitioning=auto_spmd_lowering,
      env_options_overrides=compiler_options,
      fdo_profile=fdo_profile,
  )

  opts = compile_options.executable_build_options
  if auto_spmd_lowering:
    assert mesh is not None
    opts.auto_spmd_partitioning_mesh_shape = list(mesh.shape.values())
    opts.auto_spmd_partitioning_mesh_ids = (
        sharding_specs.get_logical_mesh_ids(list(mesh.shape.values()))
        .reshape(-1))
  compile_options.parameter_is_tupled_arguments = tuple_args
  opts.allow_spmd_sharding_propagation_to_output = list(_allow_propagation_to_outputs)

  if hasattr(backend, "compile_replicated"):
    return None, compile_options

  with dispatch.log_elapsed_time(
      "Finished XLA compilation of {fun_name} in {elapsed_time} sec",
      fun_name=name, event=dispatch.BACKEND_COMPILE_EVENT):
    xla_executable = dispatch.compile_or_get_cached(
        backend, computation, dev, compile_options, host_callbacks)
  return xla_executable, compile_options
