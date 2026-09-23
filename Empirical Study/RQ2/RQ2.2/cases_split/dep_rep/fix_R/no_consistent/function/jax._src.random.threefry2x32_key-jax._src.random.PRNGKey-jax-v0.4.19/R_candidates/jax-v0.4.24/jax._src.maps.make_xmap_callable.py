@lu.cache
def make_xmap_callable(fun: lu.WrappedFun,
                       name,
                       in_axes, out_axes_thunk, donated_invars,
                       global_axis_sizes, axis_resources, resource_env, backend,
                       spmd_in_axes, spmd_out_axes_thunk,
                       lowering_parameters: mlir.LoweringParameters,
                       *in_avals):
  plan = EvaluationPlan.from_axis_resources(
      axis_resources, resource_env, global_axis_sizes)

  # TODO: Making axis substitution final style would allow us to avoid
  #       tracing to jaxpr here
  mapped_in_avals = [_delete_aval_axes(aval, in_axes, global_axis_sizes)
                     for aval, in_axes in zip(in_avals, in_axes)]
  with core.extend_axis_env_nd(global_axis_sizes.items()):
    with dispatch.log_elapsed_time(
        "Finished tracing + transforming {fun_name} for xmap in {elapsed_time} sec",
        fun_name=fun.__name__, event=dispatch.JAXPR_TRACE_EVENT):
      jaxpr, out_avals, consts = pe.trace_to_jaxpr_final(fun, mapped_in_avals)
  out_axes = out_axes_thunk()
  _check_out_avals_vs_out_axes(out_avals, out_axes, global_axis_sizes)
  # NOTE: We don't use avals and all params, so only pass in the relevant parts (too lazy...)
  _resource_typing_xmap([], dict(axis_resources=axis_resources,
                                 out_axes=out_axes,
                                 call_jaxpr=jaxpr,
                                 resource_env=resource_env,
                                 name=name),
                        source_info_util.new_source_info(), resource_env, {})
  jaxpr = plan.subst_axes_with_resources(jaxpr)
  use_spmd_lowering = SPMD_LOWERING.value
  ensure_fixed_sharding = _ENSURE_FIXED_SHARDING.value
  if use_spmd_lowering and ensure_fixed_sharding:
    jaxpr = _fix_inferred_spmd_sharding(jaxpr, resource_env)

  f = lu.wrap_init(core.jaxpr_as_fun(core.ClosedJaxpr(jaxpr, consts)))
  f = hide_mapped_axes(f, tuple(in_axes), tuple(out_axes))
  f = plan.vectorize_and_loop(f, in_axes, out_axes)

  used_resources = _jaxpr_resources(jaxpr, resource_env) | set(it.chain(*axis_resources.values()))
  used_mesh_axes = used_resources & resource_env.physical_resource_axes
  if used_mesh_axes:
    assert spmd_in_axes is None and spmd_out_axes_thunk is None  # No outer xmaps, so should be None
    mesh_in_axes, mesh_out_axes = plan.to_mesh_axes(in_axes, out_axes)
    mesh = resource_env.physical_mesh
    tiling_method: pxla.TilingMethod
    if SPMD_LOWERING_MANUAL.value:
      manual_mesh_axes = frozenset(it.chain.from_iterable(plan.physical_axis_resources.values()))
      tiling_method = pxla.TileManual(manual_mesh_axes)
    else:
      tiling_method = pxla.TileVectorize()
    in_shardings = [NamedSharding(mesh, array_mapping_to_axis_resources(i))
                    for i in mesh_in_axes]
    out_shardings = [NamedSharding(mesh, array_mapping_to_axis_resources(o))
                     for o in mesh_out_axes]
    return pxla.lower_mesh_computation(
        f, 'xmap', name, mesh,
        in_shardings, out_shardings, donated_invars,
        use_spmd_lowering, in_avals,
        tiling_method=tiling_method,
        lowering_parameters=lowering_parameters)
  else:
    jaxpr, out_avals, consts = pe.trace_to_jaxpr_final(f, in_avals)
    return pxla.lower_sharding_computation(
        core.ClosedJaxpr(jaxpr, consts), 'jit', name,
        (UNSPECIFIED,) * len(in_avals), (UNSPECIFIED,) * len(out_avals),
        donated_invars, in_avals, keep_unused=True, inline=False,
        devices_from_context=None, lowering_parameters=lowering_parameters,
        in_layouts=(None,) * len(in_avals), out_layouts=(None,) * len(out_avals))
