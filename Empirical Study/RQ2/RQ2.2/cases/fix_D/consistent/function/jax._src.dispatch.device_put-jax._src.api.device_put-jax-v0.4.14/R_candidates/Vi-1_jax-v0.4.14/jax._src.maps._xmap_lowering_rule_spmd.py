def _xmap_lowering_rule_spmd(ctx, *global_in_nodes,
                             call_jaxpr, name, in_axes, out_axes,
                             donated_invars, global_axis_sizes, spmd_in_axes,
                             spmd_out_axes, axis_resources,
                             resource_env, backend):
  xla.check_backend_matches(backend, ctx.module_context.platform)
  plan = EvaluationPlan.from_axis_resources(
      axis_resources, resource_env, global_axis_sizes)

  resource_call_jaxpr = plan.subst_axes_with_resources(call_jaxpr)
  f = lu.wrap_init(core.jaxpr_as_fun(core.ClosedJaxpr(resource_call_jaxpr, ())))
  f = hide_mapped_axes(f, in_axes, out_axes)
  f = plan.vectorize_and_loop(f, in_axes, out_axes)
  mesh_in_axes, mesh_out_axes = plan.to_mesh_axes(in_axes, out_axes)
  mesh = resource_env.physical_mesh
  f = pxla.vtile_by_mesh(f, mesh, mesh_in_axes, mesh_out_axes)

  # XXX: We modify mesh_in_axes and mesh_out_axes here
  def add_spmd_axes(
      flat_mesh_axes: Sequence[ArrayMapping],
      flat_extra_axes: Optional[Sequence[Sequence[Sequence[MeshAxisName]]]]):
    if flat_extra_axes is None:
      return
    for axes, extra in zip(flat_mesh_axes, flat_extra_axes):
      for dim, dim_extra_axis in enumerate(extra):
        if dim_extra_axis is None: continue
        assert dim_extra_axis not in axes
        assert not config.jax_enable_checks or all(v != dim for v in axes.values())
        axes[dim_extra_axis] = dim
  add_spmd_axes(mesh_in_axes, spmd_in_axes)
  add_spmd_axes(mesh_out_axes, spmd_out_axes)
  global_in_avals = ctx.avals_in
  vectorized_jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_dynamic(f, global_in_avals)

  global_sharding_spec = pxla.mesh_sharding_specs(mesh.shape, mesh.axis_names)
  sharded_global_in_nodes = [
    [mlir.wrap_with_sharding_op(
        ctx, node, aval,
        global_sharding_spec(aval, aval_axes).sharding_proto().to_proto())]
    if aval_axes else [node]
    for node, aval, aval_axes in zip(global_in_nodes, global_in_avals, mesh_in_axes)
  ]
  const_nodes = map(mlir.ir_constants, consts)

  # We in-line here rather than generating a Call HLO as in the xla_call
  # translation rule just because the extra tuple stuff is a pain.
  sub_ctx = ctx.module_context.replace(
      name_stack=ctx.module_context.name_stack.extend(wrap_name(name, 'xmap')))
  if any(effects.ordered_effects.contains(eff) for eff
         in vectorized_jaxpr.effects):
    raise NotImplementedError('Cannot lower `xmap` with ordered effects.')
  global_out_nodes, _ = mlir.jaxpr_subcomp(sub_ctx, vectorized_jaxpr,
      mlir.TokenSet(), const_nodes, *sharded_global_in_nodes,
      dim_var_values=ctx.dim_var_values)

  sharded_global_out_nodes = [
    mlir.wrap_with_sharding_op(
        ctx, node, aval,
        global_sharding_spec(aval, aval_axes).sharding_proto().to_proto())
    if aval_axes else node
    for (node,), aval, aval_axes in zip(global_out_nodes, global_out_avals, mesh_out_axes)
  ]

  return sharded_global_out_nodes
