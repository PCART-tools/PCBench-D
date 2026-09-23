@lu.cache
def make_xmap_callable(fun: lu.WrappedFun,
                       name,
                       in_axes, out_axes_thunk, donated_invars,
                       global_axis_sizes, axis_resources, resource_env, backend,
                       spmd_in_axes, spmd_out_axes_thunk, in_positional_semantics,
                       out_positional_semantics,
                       lowering_platform: Optional[str],
                       *in_avals):
  plan = EvaluationPlan.from_axis_resources(
      axis_resources, resource_env, global_axis_sizes, in_positional_semantics)

  # TODO: Making axis substitution final style would allow us to avoid
  #       tracing to jaxpr here
  mapped_in_avals = [_delete_aval_axes(aval, in_axes, global_axis_sizes)
                     for aval, in_axes in zip(in_avals, in_axes)]
  with core.extend_axis_env_nd(global_axis_sizes.items()):
    with dispatch.log_elapsed_time(f"Finished tracing + transforming {fun.__name__} "
                                   "for xmap in {elapsed_time} sec",
                                    event=dispatch.JAXPR_TRACE_EVENT):
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
  use_spmd_lowering = config.experimental_xmap_spmd_lowering
  ensure_fixed_sharding = config.experimental_xmap_ensure_fixed_sharding
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
    global_in_avals = [
        av if ips == _PositionalSemantics.GLOBAL else mesh._local_to_global(ax, av)
        for ax, av, ips in safe_zip(mesh_in_axes, in_avals, in_positional_semantics)
    ]
    in_is_global = [ips == _PositionalSemantics.GLOBAL or not ia
                    for ips, ia in safe_zip(in_positional_semantics, mesh_in_axes)]
    tiling_method: pxla.TilingMethod
    if config.experimental_xmap_spmd_lowering_manual:
      manual_mesh_axes = frozenset(it.chain.from_iterable(plan.physical_axis_resources.values()))
      tiling_method = pxla.TileManual(manual_mesh_axes)
    else:
      tiling_method = pxla.TileVectorize()
    in_shardings = [NamedSharding(mesh, pxla.array_mapping_to_axis_resources(i))
                    for i in mesh_in_axes]
    out_shardings = [NamedSharding(mesh, pxla.array_mapping_to_axis_resources(o))
                     for o in mesh_out_axes]
    return pxla.lower_mesh_computation(
        f, 'xmap', name, mesh,
        in_shardings, out_shardings, donated_invars,
        use_spmd_lowering, global_in_avals,
        tiling_method=tiling_method, in_is_global=in_is_global,
        lowering_platform=lowering_platform)
  else:
    if config.jax_array:
      return dispatch.sharded_lowering(
          f, None, backend, name, donated_invars, False, True,
          *[(a, None) for a in in_avals], lowering_platform=lowering_platform)
    else:
      return dispatch.lower_xla_callable(
          f, None, backend, name, donated_invars, False, True,
          *[(a, None) for a in in_avals], lowering_platform=lowering_platform)
