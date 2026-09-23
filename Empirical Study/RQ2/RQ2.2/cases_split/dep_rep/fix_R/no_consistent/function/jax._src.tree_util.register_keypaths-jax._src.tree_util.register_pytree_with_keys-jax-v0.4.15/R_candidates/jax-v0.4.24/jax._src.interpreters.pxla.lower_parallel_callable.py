@profiler.annotate_function
def lower_parallel_callable(
    fun: lu.WrappedFun,
    backend_name: str | None,
    axis_name: core.AxisName,
    axis_size: int,
    global_axis_size: int,
    devices: Sequence[xc.Device] | None,
    name: str,
    in_axes: Iterable[int | None],
    out_axes_thunk: Callable[[], Sequence[int | None]],
    donated_invars: Sequence[bool],
    is_explicit_global_axis_size: bool,
    avals: Sequence[core.AbstractValue],
    *,
    lowering_parameters: mlir.LoweringParameters) -> PmapComputation:
  # Determine global_axis_size for use in AxisEnv.
  # TODO(mattjj,skyewm): revive this check (inner_pmap always False now)
  # if xb.process_count() > 1 and global_axis_size is None and inner_pmap:
  #   raise ValueError("'axis_size' must be specified for nested multi-host pmaps")
  if (xb.process_count() == 1 and is_explicit_global_axis_size
      and global_axis_size != axis_size):
    raise ValueError(
        f"Specified axis_size {global_axis_size} doesn't match received "
        f"axis_size {axis_size}.")

  if devices is not None and backend_name is None:
    backend = xb.get_device_backend(devices[0])
  else:
    backend = xb.get_backend(backend_name)

  no_nested_sharding = False
  must_run_on_all_devices = False
  if not is_explicit_global_axis_size:
    if xb.process_count(backend) > 1:
      if devices:
        # This allows each host in a multi-host pmap to run on a different number
        # of devices, but precludes nested sharding (i.e. inner pmaps).
        no_nested_sharding = True
      else:
        # This assumes all hosts run on the same number of devices. We make sure
        # this assumption is true by requiring that the pmap is run on all devices
        # (and making the further assumption that each host has the same number of
        # devices). Nested sharding is ok in this case.
        must_run_on_all_devices = True

  pci = ParallelCallableInfo(
      name, backend, axis_name, axis_size, global_axis_size, devices,
      in_axes, out_axes_thunk, avals)
  jaxpr, consts, replicas, shards = stage_parallel_callable(pci, fun)
  if logger.isEnabledFor(logging.DEBUG):
    logger.debug("sharded_avals: %s", shards.sharded_avals)
    logger.debug("global_sharded_avals: %s", shards.global_sharded_avals)
    logger.debug("num_replicas: %d  num_local_replicas: %d",
                 replicas.num_global_replicas, replicas.num_local_replicas)
    logger.debug("devices: %s", devices)
    logger.debug("local_devices: %s", pci.local_devices)

  if (xb.process_count(backend) > 1 and must_run_on_all_devices and
      shards.num_local_shards != xb.local_device_count(backend)):
    if shards.num_local_shards == axis_size:
      raise ValueError(
         f"On multi-host platforms, the input to pmapped functions must have "
         f"leading axis size equal to the number of local devices if no "
         f"`devices` argument is specified. Got {axis_size=}, "
         f"num_local_devices={xb.local_device_count(backend)}")
    else:
      raise ValueError(
        f"On multi-host platforms, pmapped functions must run across all "
        f"devices, i.e. num_replicas * num_partitions should equal the "
        f"number of local devices. Got "
        f"num_replicas={replicas.num_local_replicas}, and "
        f"num_local_devices={xb.local_device_count(backend)}")

  if no_nested_sharding and replicas.jaxpr_replicas > 1:
    raise ValueError(
      f"On multi-host platforms, pmapped functions that both have `devices` "
      f"specified and contain an inner_pmap must specify an "
      f"`axis_size` (or remove the `devices` argument). Got nested_replicas="
      f"{replicas.jaxpr_replicas}")

  log_priority = logging.WARNING if config.log_compiles.value else logging.DEBUG
  if logger.isEnabledFor(log_priority):
    logger.log(log_priority,
               "Compiling %s (%d) for %d devices with args %s. (num_replicas=%d)",
               fun.__name__, id(fun),
               shards.num_global_shards, avals, replicas.num_global_replicas)

  axis_env = sharding_impls.AxisEnv(
      replicas.num_global_replicas, (axis_name,), (global_axis_size,))
  name_stack = source_info_util.new_name_stack(wrap_name(name, 'pmap'))
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  replicated_args = [axis is None for axis in in_axes]
  tuple_args = dispatch.should_tuple_args(len(shards.global_sharded_avals),
                                          backend.platform)
  module_name = f"pmap_{fun.__name__}"
  with maybe_extend_axis_env(axis_name, global_axis_size, None):  # type: ignore
    ordered_effects = list(
        effects.ordered_effects.filter_in(closed_jaxpr.effects))
    if ordered_effects:
      raise ValueError("Ordered effects not supported in `pmap`.")
    unordered_effects = list(
        effects.ordered_effects.filter_not_in(closed_jaxpr.effects))
    with dispatch.log_elapsed_time(
        "Finished jaxpr to MLIR module conversion {fun_name} in {elapsed_time} sec",
        fun_name=str(name_stack), event=dispatch.JAXPR_TO_MLIR_MODULE_EVENT):
      lowering_result = mlir.lower_jaxpr_to_module(
          module_name,
          closed_jaxpr,
          ordered_effects=ordered_effects,
          backend_or_name=backend,
          platforms=lowering_parameters.platforms or (backend.platform,),
          axis_context=sharding_impls.ReplicaAxisContext(axis_env),
          name_stack=name_stack,
          donated_args=donated_invars,
          replicated_args=replicated_args,
          arg_shardings=None,
          result_shardings=None,
          arg_names=jaxpr.debug_info and jaxpr.debug_info.arg_names,
          result_names=jaxpr.debug_info and jaxpr.debug_info.result_paths,
          num_replicas=replicas.num_global_replicas,
          lowering_parameters=lowering_parameters)
  return PmapComputation(lowering_result.module, pci=pci, replicas=replicas,
                         shards=shards, tuple_args=tuple_args,
                         unordered_effects=unordered_effects,
                         ordered_effects=ordered_effects,
                         keepalive=lowering_result.keepalive,
                         host_callbacks=lowering_result.host_callbacks,
                         jaxpr_debug_info=closed_jaxpr.jaxpr.debug_info)
