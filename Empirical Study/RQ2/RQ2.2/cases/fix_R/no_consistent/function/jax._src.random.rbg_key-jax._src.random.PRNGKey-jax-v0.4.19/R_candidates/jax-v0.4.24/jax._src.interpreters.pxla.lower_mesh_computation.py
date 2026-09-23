@profiler.annotate_function
def lower_mesh_computation(
    fun_or_jaxpr: lu.WrappedFun | core.ClosedJaxpr,
    api_name: str,
    fun_name: str,
    mesh: Mesh,
    in_shardings: Sequence[sharding_impls.NamedSharding | AUTO],
    out_shardings: Sequence[(sharding_impls.NamedSharding | AUTO |
                                  UnspecifiedValue)],
    donated_invars: Sequence[bool],
    spmd_lowering: bool,
    global_in_avals: Sequence[core.ShapedArray],
    tiling_method: TilingMethod | None,
    lowering_parameters: mlir.LoweringParameters) -> MeshComputation:
  assert not mesh.empty
  backend = xb.get_device_backend(mesh.devices.flat[0])
  name_stack = source_info_util.new_name_stack(wrap_name(fun_name, api_name))

  global_axis_sizes = mesh.shape

  log_priority = logging.WARNING if config.log_compiles.value else logging.DEBUG
  if logger.isEnabledFor(log_priority):
    logger.log(log_priority,
               "Compiling %s for %s mesh with global shapes and types %s. "
               "Argument mapping: %s.",
               fun_name, tuple(global_axis_sizes.items()), global_in_avals,
               in_shardings)

  # 1. Trace to jaxpr and preprocess/verify it
  if spmd_lowering:
    manual_axes: frozenset[MeshAxisName] = frozenset()
    # TODO: Consider handling xmap's 'vectorize' in here. We can vmap once instead of vtile twice!
    if tiling_method is not None:
      if isinstance(tiling_method, TileVectorize):
        tiling_transform = vtile_by_mesh
      elif isinstance(tiling_method, TileManual):
        tiling_transform = lambda f, *args: vtile_manual(f, tiling_method.manual_axes, *args)  # type: ignore
        manual_axes = tiling_method.manual_axes
      else:
        raise NotImplementedError(f"Unrecognized tiling method: {tiling_method}")
      assert not callable(out_shardings)
      assert isinstance(fun_or_jaxpr, lu.WrappedFun)
      # This is the xmap path where there is no `AUTO` or `UNSPECIFIED`, which
      # is why `.spec` can be accessed.
      fun_or_jaxpr = tiling_transform(
          fun_or_jaxpr, mesh, [get_array_mapping(i.spec) for i in in_shardings],  # type: ignore
          [get_array_mapping(o.spec) for o in out_shardings])  # type: ignore
    in_jaxpr_avals = global_in_avals
  else:
    assert isinstance(tiling_method, TileVectorize)
    # In non-spmd lowering path, there is no `AUTO` or `UNSPECIFIED`, which is
    # why `.spec` can be accessed.
    in_tiled_avals = [tile_aval_nd(global_axis_sizes, get_array_mapping(i.spec), aval)  # type: ignore
                      for aval, i in safe_zip(global_in_avals, in_shardings)]
    in_jaxpr_avals = in_tiled_avals

  with core.extend_axis_env_nd(mesh.shape.items()):
    if isinstance(fun_or_jaxpr, lu.WrappedFun):
      with dispatch.log_elapsed_time(
          "Finished tracing + transforming {fun_name} in {elapsed_time} sec",
          fun_name=str(name_stack), event=dispatch.JAXPR_TRACE_EVENT):
        jaxpr, out_jaxpr_avals, consts = pe.trace_to_jaxpr_final(
            fun_or_jaxpr, in_jaxpr_avals)
    else:
      assert isinstance(fun_or_jaxpr, core.ClosedJaxpr)
      jaxpr = fun_or_jaxpr.jaxpr
      out_jaxpr_avals = fun_or_jaxpr.out_avals
      consts = fun_or_jaxpr.consts

  all_args_info = AllArgsInfo(global_in_avals, in_shardings, jaxpr.debug_info)

  assert len(out_shardings) == len(out_jaxpr_avals)
  if spmd_lowering:
    global_out_avals = out_jaxpr_avals
  else:
    # In non-spmd lowering path, there is no `AUTO` or `UNSPECIFIED`, which is
    # why `.spec` can be accessed.
    global_out_avals = [untile_aval_nd(global_axis_sizes, get_array_mapping(o.spec), aval)  # type: ignore
                        for aval, o in safe_zip(out_jaxpr_avals, out_shardings)]

  _sanitize_mesh_jaxpr(jaxpr)
  jaxpr = dispatch.apply_outfeed_rewriter(jaxpr)

  # 2. Build up the HLO
  tuple_args = dispatch.should_tuple_args(len(in_jaxpr_avals), backend.platform)

  in_partitions: list[sharding_impls.XLACompatibleSharding | None] | None
  out_partitions: list[sharding_impls.XLACompatibleSharding | None] | None
  axis_ctx: mlir.AxisContext
  if spmd_lowering:
    in_partitions = map(_to_logical_sharding, global_in_avals, in_shardings)
    out_partitions = map(_to_logical_sharding, global_out_avals, out_shardings)
    replicated_args = [False] * len(in_jaxpr_avals)
    axis_ctx = sharding_impls.SPMDAxisContext(mesh, manual_axes)
    num_replicas = 1
    num_partitions = mesh.devices.size
  else:
    replicated_args = [not get_array_mapping(i.spec) for i in in_shardings]  # type: ignore
    in_partitions = None
    out_partitions = None
    axis_env = sharding_impls.AxisEnv(
        nreps=mesh.size,
        names=tuple(global_axis_sizes.keys()),
        sizes=tuple(global_axis_sizes.values()))
    axis_ctx = sharding_impls.ReplicaAxisContext(axis_env)
    num_replicas = mesh.devices.size
    num_partitions = 1
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  module_name = f"{api_name}_{fun_name}"
  with core.extend_axis_env_nd(mesh.shape.items()):
    if any(effects.ordered_effects.contains(eff) for eff
           in closed_jaxpr.effects):
      raise ValueError("Ordered effects not supported in mesh computations.")
    unordered_effects = list(effects.ordered_effects.filter_not_in(
      closed_jaxpr.effects))
    ordered_effects = list(effects.ordered_effects.filter_in(
      closed_jaxpr.effects))
    with dispatch.log_elapsed_time(
        "Finished jaxpr to MLIR module conversion {fun_name} in {elapsed_time} sec",
        fun_name=str(name_stack), event=dispatch.JAXPR_TO_MLIR_MODULE_EVENT):
      lowering_result = mlir.lower_jaxpr_to_module(
          module_name,
          closed_jaxpr,
          ordered_effects=ordered_effects,
          backend_or_name=backend,
          platforms=lowering_parameters.platforms or (backend.platform,),
          axis_context=axis_ctx,
          name_stack=name_stack,
          donated_args=donated_invars,
          replicated_args=replicated_args,
          arg_shardings=in_partitions,
          result_shardings=out_partitions,
          arg_names=jaxpr.debug_info and jaxpr.debug_info.arg_names,
          result_names=jaxpr.debug_info and jaxpr.debug_info.result_paths,
          num_replicas=num_replicas,
          num_partitions=num_partitions,
          lowering_parameters=lowering_parameters)

  return MeshComputation(
      str(name_stack),
      lowering_result.module,
      donated_invars,
      global_in_avals=global_in_avals,
      global_out_avals=global_out_avals,
      in_shardings=in_shardings,
      out_shardings=out_shardings,
      spmd_lowering=spmd_lowering,
      tuple_args=tuple_args,
      auto_spmd_lowering=False,
      unordered_effects=unordered_effects,
      ordered_effects=ordered_effects,
      host_callbacks=lowering_result.host_callbacks,
      keepalive=lowering_result.keepalive,
      kept_var_idx=set(range(len(global_in_avals))),
      backend=backend,
      device_assignment=_create_da_object(tuple(mesh.devices.flat)),
      committed=True,
      in_layouts=(None,) * len(global_in_avals),
      out_layouts=(None,) * len(global_out_avals),
      shape_poly_state=lowering_result.shape_poly_state,
      all_args_info=all_args_info)
