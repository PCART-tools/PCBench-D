@weakref_lru_cache
def _cached_lowering_to_hlo(closed_jaxpr, api_name, fun_name, backend,
                            semantic_in_shardings, semantic_out_shardings,
                            in_layouts, out_layouts, num_devices, device_assignment,
                            donated_invars, name_stack, all_default_mem_kind,
                            lowering_parameters: mlir.LoweringParameters):
  jaxpr = closed_jaxpr.jaxpr
  in_shardings = semantic_in_shardings.shardings
  out_shardings = semantic_out_shardings.shardings
  global_in_avals = closed_jaxpr.in_avals
  global_out_avals = closed_jaxpr.out_avals

  log_priority = logging.WARNING if config.log_compiles.value else logging.DEBUG
  if logger.isEnabledFor(log_priority):
    logger.log(log_priority,
               "Compiling %s for with global shapes and types %s. "
               "Argument mapping: %s.",
               fun_name, global_in_avals, in_shardings)

  # Look at the number of replcas present in the jaxpr. In
  # lower_sharding_computation, nreps > 1 during `jit(pmap)` cases. This is
  # handled here so as to deprecate the lower_xla_callable codepath when
  # `jax.Array` is turned on by default.
  # TODO(yashkatariya): Remove this when `jit(pmap)` is removed.
  nreps = dispatch.jaxpr_replicas(jaxpr)
  _raise_warnings_or_errors_for_jit_of_pmap(nreps, backend, fun_name, jaxpr)

  in_mlir_shardings: list[sharding_impls.XLACompatibleSharding | None] | None
  out_mlir_shardings: list[sharding_impls.XLACompatibleSharding | None] | None
  axis_ctx: mlir.AxisContext

  if nreps == 1:
    in_mlir_shardings = map(_to_logical_sharding, global_in_avals, in_shardings)
    out_mlir_shardings = map(_to_logical_sharding, global_out_avals, out_shardings)
    replicated_args = [False] * len(global_in_avals)
    axis_ctx = sharding_impls.ShardingContext(num_devices, device_assignment)
    num_partitions = num_devices
  else:
    # This path is triggered for `jit(pmap)` cases.
    replicated_args = None
    in_mlir_shardings = None
    out_mlir_shardings = None
    axis_env = sharding_impls.AxisEnv(nreps, (), ())
    axis_ctx = sharding_impls.ReplicaAxisContext(axis_env)
    num_partitions = 1

  module_name = f"{api_name}_{fun_name}"

  if num_devices > 1:
    unsupported_effects = effects.ordered_effects.filter_in(closed_jaxpr.effects)
    unsupported_effects = effects.shardable_ordered_effects.filter_not_in(
        unsupported_effects)
    if len(unsupported_effects) > 0:
      raise ValueError(
        "The following ordered effects are not supported for "
        f"more than 1 device: {unsupported_effects}")
  ordered_effects = list(effects.ordered_effects.filter_in(closed_jaxpr.effects))

  with dispatch.log_elapsed_time(
        "Finished jaxpr to MLIR module conversion {fun_name} in {elapsed_time} sec",
        fun_name=str(name_stack), event=dispatch.JAXPR_TO_MLIR_MODULE_EVENT):
    lowering_result = mlir.lower_jaxpr_to_module(
        module_name,
        closed_jaxpr,
        ordered_effects=ordered_effects,
        backend_or_name=backend,
        # Optionally, override the lowering platform
        platforms=lowering_parameters.platforms or (backend.platform,),
        axis_context=axis_ctx,
        name_stack=name_stack,
        donated_args=donated_invars,
        replicated_args=replicated_args,
        arg_shardings=in_mlir_shardings,
        result_shardings=out_mlir_shardings,
        in_layouts=in_layouts,
        out_layouts=out_layouts,
        arg_names=jaxpr.debug_info and jaxpr.debug_info.arg_names,
        result_names=jaxpr.debug_info and jaxpr.debug_info.result_paths,
        num_replicas=nreps,
        num_partitions=num_partitions,
        all_default_mem_kind=all_default_mem_kind,
        lowering_parameters=lowering_parameters)
  tuple_args = dispatch.should_tuple_args(len(global_in_avals), backend.platform)
  unordered_effects = list(
      effects.ordered_effects.filter_not_in(closed_jaxpr.effects))
  return (lowering_result.module, lowering_result.keepalive,
          lowering_result.host_callbacks, unordered_effects, ordered_effects,
          nreps, tuple_args, lowering_result.shape_poly_state)
