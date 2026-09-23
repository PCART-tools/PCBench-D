def _xmap_lowering_rule_spmd_manual(ctx, *global_in_nodes,
                                    call_jaxpr, name, in_axes, out_axes,
                                    donated_invars, global_axis_sizes, spmd_in_axes,
                                    spmd_out_axes, in_positional_semantics,
                                    out_positional_semantics, axis_resources,
                                    resource_env, backend):
  assert spmd_in_axes is None and spmd_out_axes is None
  # This first part (up to vtile_manual) is shared with non-MANUAL SPMD rule.
  xla.check_backend_matches(backend, ctx.module_context.platform)
  plan = EvaluationPlan.from_axis_resources(
      axis_resources, resource_env, global_axis_sizes, in_positional_semantics)
  manual_mesh_axes = frozenset(it.chain.from_iterable(plan.physical_axis_resources.values()))

  resource_call_jaxpr = plan.subst_axes_with_resources(call_jaxpr)
  f = lu.wrap_init(core.jaxpr_as_fun(core.ClosedJaxpr(resource_call_jaxpr, ())))
  f = hide_mapped_axes(f, in_axes, out_axes)
  f = plan.vectorize_and_loop(f, in_axes, out_axes)

  # NOTE: Sharding constraints are handled entirely by vtile_manual!
  mesh_in_axes, mesh_out_axes = plan.to_mesh_axes(in_axes, out_axes)
  mesh = resource_env.physical_mesh
  f = pxla.vtile_manual(f, tuple(manual_mesh_axes), mesh, mesh_in_axes, mesh_out_axes)

  # NOTE: We don't extend the resource env with the mesh shape, because those
  #       resources are already in scope! It's the outermost xmap that introduces
  #       them!
  global_in_avals = ctx.avals_in
  vectorized_jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_dynamic(f, global_in_avals)
  const_nodes = map(mlir.ir_constants, consts)

  # We in-line here rather than generating a Call HLO as in the xla_call
  # translation rule just because the extra tuple stuff is a pain.
  assert isinstance(ctx.module_context.axis_context, mlir.SPMDAxisContext)
  sub_ctx = ctx.module_context.replace(
      name_stack=ctx.module_context.name_stack.extend(wrap_name(name, 'xmap')),
      axis_context=ctx.module_context.axis_context.extend_manual(manual_mesh_axes))
  if any(effects.ordered_effects.contains(eff) for eff
         in vectorized_jaxpr.effects):
    raise NotImplementedError('Cannot lower `xmap` with ordered effects.')
  global_out_nodes, _ = mlir.jaxpr_subcomp(sub_ctx, vectorized_jaxpr,
      mlir.TokenSet(), const_nodes, *([n] for n in global_in_nodes),
      dim_var_values=ctx.dim_var_values)

  return global_out_nodes
