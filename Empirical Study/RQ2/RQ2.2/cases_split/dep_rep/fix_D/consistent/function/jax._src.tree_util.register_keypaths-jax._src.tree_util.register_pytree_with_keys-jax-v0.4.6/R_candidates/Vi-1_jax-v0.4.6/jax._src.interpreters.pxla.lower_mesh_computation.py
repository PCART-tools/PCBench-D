@profiler.annotate_function
def lower_mesh_computation(
    fun_or_jaxpr: Union[lu.WrappedFun, core.ClosedJaxpr],
    api_name: str,
    fun_name: str,
    mesh: Mesh,
    in_shardings: Sequence[Union[sharding_internal.NamedSharding, AUTOAxisResource]],
    out_shardings: Sequence[Union[sharding_internal.NamedSharding, AUTOAxisResource,
                            UnspecifiedValue]],
    donated_invars: Sequence[bool],
    spmd_lowering: bool,
    global_in_avals: Sequence[core.ShapedArray],
    tiling_method: Optional[TilingMethod],
    in_is_global: Sequence[bool],
    lowering_platform: Optional[str]) -> MeshComputation:
  assert not mesh.empty
  backend = xb.get_device_backend(mesh.devices.flat[0])
  name_stack = source_info_util.new_name_stack(wrap_name(fun_name, api_name))

  auto_spmd_lowering = check_if_any_auto(in_shardings + out_shardings)  # type: ignore

  if auto_spmd_lowering and not spmd_lowering:
    raise ValueError('Enable spmd_lowering to use auto spmd lowering.')

  global_axis_sizes = mesh.shape

  log_priority = logging.WARNING if config.jax_log_compiles else logging.DEBUG
  logger.log(log_priority,
              "Compiling %s for %s mesh with global shapes and types %s. "
              "Argument mapping: %s.",
              fun_name, tuple(global_axis_sizes.items()), global_in_avals,
              in_shardings)

  # 1. Trace to jaxpr and preprocess/verify it
  if spmd_lowering:
    manual_axes: FrozenSet[MeshAxisName] = frozenset()
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
      assert not auto_spmd_lowering
      assert isinstance(fun_or_jaxpr, lu.WrappedFun)
      # This is the xmap path where there is no `AUTO` or `UNSPECIFIED`, which
      # is why `.spec` can be accessed.
      fun_or_jaxpr = tiling_transform(
          fun_or_jaxpr, mesh, [get_array_mapping(i.spec) for i in in_shardings],  # type: ignore
          [get_array_mapping(o.spec) for o in out_shardings])  # type: ignore
    in_jaxpr_avals = global_in_avals
  else:
    assert isinstance(tiling_method, TileVectorize)
    assert not auto_spmd_lowering
    # In non-spmd lowering path, there is no `AUTO` or `UNSPECIFIED`, which is
    # why `.spec` can be accessed.
    in_tiled_avals = [tile_aval_nd(global_axis_sizes, get_array_mapping(i.spec), aval)  # type: ignore
                      for aval, i in safe_zip(global_in_avals, in_shardings)]
    in_jaxpr_avals = in_tiled_avals

  with core.extend_axis_env_nd(mesh.shape.items()):
    if isinstance(fun_or_jaxpr, lu.WrappedFun):
      with dispatch.log_elapsed_time(
          f"Finished tracing + transforming {name_stack} in "
          "{elapsed_time} sec", event=dispatch.JAXPR_TRACE_EVENT):
        jaxpr, out_jaxpr_avals, consts = pe.trace_to_jaxpr_final(
            fun_or_jaxpr, in_jaxpr_avals)
    else:
      assert isinstance(fun_or_jaxpr, core.ClosedJaxpr)
      jaxpr = fun_or_jaxpr.jaxpr
      out_jaxpr_avals = fun_or_jaxpr.out_avals
      consts = fun_or_jaxpr.consts

  assert len(out_shardings) == len(out_jaxpr_avals)
  if spmd_lowering:
    global_out_avals = out_jaxpr_avals
  else:
    # In non-spmd lowering path, there is no `AUTO` or `UNSPECIFIED`, which is
    # why `.spec` can be accessed.
    global_out_avals = [untile_aval_nd(global_axis_sizes, get_array_mapping(o.spec), aval)  # type: ignore
                        for aval, o in safe_zip(out_jaxpr_avals, out_shardings)]

  _sanitize_mesh_jaxpr(jaxpr)
  if mesh.is_multi_process:
    check_multihost_collective_allowlist(jaxpr)
  jaxpr = dispatch.apply_outfeed_rewriter(jaxpr)

  # 2. Build up the HLO
  tuple_args = dispatch.should_tuple_args(len(in_jaxpr_avals), backend.platform)

  in_partitions: Optional[List[Optional[xc.OpSharding]]]
  out_partitions: Optional[List[Optional[xc.OpSharding]]]
  axis_ctx: mlir.AxisContext
  if spmd_lowering:
    in_partitions = []
    for aval, i in safe_zip(global_in_avals, in_shardings):
      if is_auto(i):
        in_partitions.append(None)
      elif core.is_opaque_dtype(aval.dtype):
        in_partitions.append(aval.dtype._rules.physical_op_sharding(aval, i))
      else:
        in_partitions.append(i._to_xla_op_sharding(aval.ndim))  # type: ignore[union-attr]

    # TODO(yashkatariya): Fix the HLO produced if out_partitions is
    # [None, OpShardingProto] has the sharding annotations.
    out_partitions = []
    for aval, o in safe_zip(global_out_avals, out_shardings):
      if is_auto(o) or _is_unspecified(o):
        out_partitions.append(None)
      elif core.is_opaque_dtype(aval.dtype):
        out_partitions.append(aval.dtype._rules.physical_op_sharding(aval, o))
      else:
        out_partitions.append(o._to_xla_op_sharding(aval.ndim))  # type: ignore[union-attr]
    replicated_args = [False] * len(in_jaxpr_avals)
    axis_ctx = mlir.SPMDAxisContext(mesh, manual_axes)
  else:
    replicated_args = [not get_array_mapping(i.spec) for i in in_shardings]  # type: ignore
    in_partitions = None
    out_partitions = None
    axis_env = xla.AxisEnv(nreps=mesh.size,
                           names=tuple(global_axis_sizes.keys()),
                           sizes=tuple(global_axis_sizes.values()))
    axis_ctx = mlir.ReplicaAxisContext(axis_env)
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  module: Union[str, xc.XlaComputation]
  module_name = f"{api_name}_{fun_name}"
  with core.extend_axis_env_nd(mesh.shape.items()):
    if any(effects.ordered_effects.contains(eff) for eff
           in closed_jaxpr.effects):
      raise ValueError("Ordered effects not supported in mesh computations.")
    unordered_effects = list(effects.ordered_effects.filter_not_in(
      closed_jaxpr.effects))
    ordered_effects = list(effects.ordered_effects.filter_in(
      closed_jaxpr.effects))
    arg_names, result_names = _debug_names(jaxpr.debug_info)
    lowering_result = mlir.lower_jaxpr_to_module(
        module_name,
        closed_jaxpr,
        unordered_effects,
        ordered_effects,
        backend,
        lowering_platform or backend.platform,
        axis_ctx,
        name_stack,
        donated_invars,
        replicated_args=replicated_args,
        arg_shardings=in_partitions,
        result_shardings=out_partitions,
        arg_names=arg_names,
        result_names=result_names)
    module, keepalive, host_callbacks = (
        lowering_result.module, lowering_result.keepalive,
        lowering_result.host_callbacks)
  return MeshComputation(
      str(name_stack),
      module,
      False,
      donated_invars,
      mesh=mesh,
      global_in_avals=global_in_avals,
      global_out_avals=global_out_avals,
      in_shardings=in_shardings,
      out_shardings=out_shardings,
      spmd_lowering=spmd_lowering,
      tuple_args=tuple_args,
      in_is_global=in_is_global,
      auto_spmd_lowering=auto_spmd_lowering,
      unordered_effects=unordered_effects,
      ordered_effects=ordered_effects,
      host_callbacks=host_callbacks,
      keepalive=keepalive,
      kept_var_idx=set(range(len(global_in_avals))),
      backend=backend,
      device_assignment=list(mesh.devices.flat),
      committed=True)
