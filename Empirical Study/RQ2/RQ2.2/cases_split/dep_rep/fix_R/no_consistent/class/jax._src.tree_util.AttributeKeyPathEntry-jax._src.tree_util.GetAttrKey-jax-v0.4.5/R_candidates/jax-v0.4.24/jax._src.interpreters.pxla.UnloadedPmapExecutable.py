@dataclasses.dataclass
class UnloadedPmapExecutable:
  compiled: Any
  backend: xb.XlaBackend
  local_input_avals: Sequence[core.AbstractValue]
  input_shardings: Sequence[sharding_impls.XLACompatibleSharding]
  local_output_avals: Sequence[ShapedArray]
  output_shardings: Sequence[sharding_impls.XLACompatibleSharding]
  unordered_effects: list[core.Effect]
  ordered_effects: list[core.Effect]
  keepalive: Sequence[Any]
  host_callbacks: Sequence[Any]
  jaxpr_debug_info: core.JaxprDebugInfo

  def build_execute_fun(self):
    input_indices = []
    for aval, spec in safe_zip(self.local_input_avals, self.input_shardings):
      assert isinstance(spec, sharding_impls.PmapSharding), spec
      assert isinstance(aval, core.ShapedArray), aval
      input_indices.append(
          sharding_specs.spec_to_indices(aval.shape, spec.sharding_spec)
          if spec.sharding_spec is not None else None)
    handle_outs = local_avals_to_results_handler(self.local_output_avals,
                                                 self.output_shardings)
    handle_args = InputsHandler(self.input_shardings,
                                self.compiled.local_devices(), input_indices)
    execute_fun = ExecuteReplicated(self.compiled, "parallel computation",
                                    self.backend, handle_args, handle_outs,
                                    self.unordered_effects,
                                    self.ordered_effects, self.keepalive,
                                    bool(self.host_callbacks),
                                    set(range(len(input_indices))))
    return execute_fun

  def load(self) -> PmapExecutable:
    fingerprint = getattr(self.compiled, "fingerprint", None)

    return PmapExecutable(
        self.compiled, self.build_execute_fun, fingerprint,
        self.local_input_avals, self.jaxpr_debug_info, self)

  @staticmethod
  def from_hlo(hlo: ir.Module,
               pci: ParallelCallableInfo,
               replicas: ReplicaInfo,
               shards: ShardInfo,
               tuple_args: bool,
               unordered_effects: list[core.Effect],
               ordered_effects: list[core.Effect],
               host_callbacks: list[Any],
               keepalive: Any,
               jaxpr_debug_info: core.JaxprDebugInfo,
               compiler_options=None):
    devices = pci.devices
    if devices is None:
      if shards.num_global_shards > xb.device_count(pci.backend):
        msg = ("compiling computation that requires {} logical devices, but only {} XLA "
               "devices are available (num_replicas={})")
        raise ValueError(msg.format(shards.num_global_shards,
                                    xb.device_count(pci.backend),
                                    replicas.num_global_replicas))
      # On a single host, we simply grab the first N devices from jax.devices().
      # In the single host case, we want the default device order of pmap to
      # match jax.devices().
      # On multiple hosts, we create a default device assignment that ensures
      # each host is responsible for a contiguous set of replicas.
      if shards.num_global_shards > shards.num_local_shards:
        # TODO(skye): use a locality-aware assignment that satisfies the above
        # constraint.
        devices = [d for process_index in range(xb.process_count(pci.backend))
                  for d in xb.local_devices(process_index, pci.backend)]
      else:
        devices = xb.local_devices(backend=pci.backend)[:shards.num_local_shards]
    else:
      if shards.num_local_shards != len(pci.local_devices):
        local_devices_str = ", ".join(map(str, pci.local_devices))
        if shards.num_local_shards == pci.axis_size:
          raise ValueError(
              f"Leading axis size of input to pmapped function must equal the "
              f"number of local devices passed to pmap. Got axis_size="
              f"{pci.axis_size}, num_local_devices={len(pci.local_devices)}.\n"
              f"(Local devices available to pmap: {local_devices_str})")
        else:
          raise ValueError(
              f"pmapped function requires {shards.num_local_shards} local "
              f"devices to run due to nested pmapped or other parallel "
              f"functions, but only {len(pci.local_devices)} are available.\n"
              f"(outer axis size: {pci.axis_size}, local devices available to "
              f"pmap: {local_devices_str})")
      if shards.num_global_shards != len(devices):
        raise ValueError("compiling computation that creates %s shards, "
                        "but %s devices were specified" %
                        (shards.num_global_shards, len(devices)))

    # 'devices' may be 1D or 2D at this point (e.g.
    # get_default_device_assignment() returns 2D assignment, caller may have
    # provided 1D list of devices).
    # Convert to 2D in case it's 1D and we have > 1 partitions.
    num_partitions = 1
    device_assignment: np.ndarray = np.array(devices).reshape(
        (replicas.num_global_replicas, num_partitions))
    compile_options = compiler.get_compile_options(
        num_replicas=replicas.num_global_replicas,
        num_partitions=num_partitions,
        device_assignment=device_assignment,
        use_spmd_partitioning=False,
        env_options_overrides=compiler_options,
        detailed_logging=compiler.use_detailed_logging(hlo),
        backend=pci.backend,
    )
    compile_options.parameter_is_tupled_arguments = tuple_args

    process_index = xb.process_index(pci.backend)
    local_device_assignment = np.array([
        d for d in device_assignment.flat if d.process_index == process_index
    ])

    input_sharding_specs = [
        sharding_specs.pmap_sharding_spec(
            replicas.num_local_replicas, pci.axis_size,
            cast(ShapedArray, aval).shape, in_axis)
        for aval, in_axis in safe_zip(shards.sharded_avals, pci.in_axes)]
    in_shardings = _get_pmap_sharding(local_device_assignment,
                                      input_sharding_specs)

    local_unmapped_avals = [
        _cast_to_shaped_array(
            _pmap_unmapped_aval(pci.axis_size, pci.axis_name, out_axis, aval))
        if out_axis is not None else aval
        for aval, out_axis in safe_zip(shards.out_sharded_avals, pci.out_axes)]
    out_specs = [
        sharding_specs.pmap_sharding_spec(
            replicas.num_local_replicas, pci.axis_size, aval.shape, out_axis)
        for aval, out_axis in safe_zip(
            shards.out_sharded_avals, pci.out_axes)]
    out_shardings = _get_pmap_sharding(local_device_assignment, out_specs)

    if hasattr(pci.backend, "compile_replicated"):
      input_indices = [
          sharding_specs.spec_to_indices(aval.shape, spec)
          if spec is not None else None
          for aval, spec in safe_zip(pci.avals, input_sharding_specs)
      ]
      handle_outs = local_avals_to_results_handler(local_unmapped_avals,
                                                   out_shardings)
      return _compile_replicated_pmap_executable_from_hlo(
          hlo, pci, input_indices, in_shardings, handle_outs,
          compile_options, host_callbacks, bool(unordered_effects),
          ordered_effects, jaxpr_debug_info)

    with dispatch.log_elapsed_time(
        "Finished XLA compilation of {fun_name} in {elapsed_time} sec",
        fun_name=pci.name, event=dispatch.BACKEND_COMPILE_EVENT):
      compiled = compiler.compile_or_get_cached(
          pci.backend, hlo, device_assignment, compile_options,
          host_callbacks)

    return UnloadedPmapExecutable(
        compiled=compiled,
        backend=pci.backend,
        local_input_avals=pci.avals,
        input_shardings=in_shardings,
        local_output_avals=local_unmapped_avals,
        output_shardings=out_shardings,
        unordered_effects=unordered_effects,
        ordered_effects=ordered_effects,
        keepalive=keepalive,
        host_callbacks=host_callbacks,
        jaxpr_debug_info=jaxpr_debug_info).load()
