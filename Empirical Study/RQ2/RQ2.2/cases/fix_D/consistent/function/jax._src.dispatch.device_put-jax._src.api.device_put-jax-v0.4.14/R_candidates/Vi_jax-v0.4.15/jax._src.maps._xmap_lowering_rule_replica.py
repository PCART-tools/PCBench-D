def _xmap_lowering_rule_replica(ctx, *in_nodes,
                                call_jaxpr, name,
                                in_axes, out_axes, donated_invars,
                                global_axis_sizes,
                                spmd_in_axes, spmd_out_axes,
                                axis_resources, resource_env, backend):
  mlir.check_backend_matches(backend, ctx.module_context.platform)
  # The only way for any of those two assertions to be violated is when xmap
  # is using the SPMD lowering, but then this rule shouldn't even trigger.
  assert spmd_in_axes is None and spmd_out_axes is None
  plan = EvaluationPlan.from_axis_resources(
      axis_resources, resource_env, global_axis_sizes)

  axis_resource_count = _get_axis_resource_count(
      axis_resources, resource_env)
  if any(resource_count.distributed for resource_count in axis_resource_count.values()):
    raise NotImplementedError

  mesh = resource_env.physical_mesh
  mesh_in_axes, mesh_out_axes = plan.to_mesh_axes(in_axes, out_axes)

  local_avals = [pxla.tile_aval_nd(
                    mesh.shape, aval_mesh_in_axes,
                    _insert_aval_axes(v.aval, aval_in_axes, global_axis_sizes))
                 for v, aval_in_axes, aval_mesh_in_axes
                 in zip(call_jaxpr.invars, in_axes, mesh_in_axes)]
  # We have to substitute before tracing, because we want the vectorized
  # axes to be used in the jaxpr.
  resource_call_jaxpr = plan.subst_axes_with_resources(call_jaxpr)
  f = lu.wrap_init(core.jaxpr_as_fun(core.ClosedJaxpr(resource_call_jaxpr, ())))
  f = hide_mapped_axes(f, tuple(in_axes), tuple(out_axes))
  f = plan.vectorize_and_loop(f, in_axes, out_axes)
  # NOTE: We don't extend the resource env with the mesh shape, because those
  #       resources are already in scope! It's the outermost xmap that introduces
  #       them!
  vectorized_jaxpr, out_avals, consts = pe.trace_to_jaxpr_dynamic(f, local_avals)
  _check_out_avals_vs_out_axes(out_avals, out_axes, global_axis_sizes)
  const_nodes = [mlir.ir_constants(xla.canonicalize_dtype(x)) for x in consts]

  local_mesh_shape = mesh.local_mesh.shape
  tiled_ins = (
    mlir.lower_fun(partial(_tile, in_axes=arg_in_axes,
                           axis_sizes=local_mesh_shape),
                   multiple_results=False)(
          ctx.replace(primitive=None,
                      avals_in=[aval], avals_out=None),
          in_node)[0]
    for v, aval, in_node, arg_in_axes
    in zip(call_jaxpr.invars, ctx.avals_in, in_nodes, mesh_in_axes))

  # NOTE: We don't extend the resource env with the mesh shape, because those
  #       resources are already in scope! It's the outermost xmap that introduces
  #       them!
  # We in-line here rather than generating a Call HLO as in the xla_call
  # translation rule just because the extra tuple stuff is a pain.
  sub_ctx = ctx.module_context.replace(
      name_stack=ctx.module_context.name_stack.extend(wrap_name(name, 'xmap')))
  if any(effects.ordered_effects.contains(eff) for eff
         in vectorized_jaxpr.effects):
    raise NotImplementedError('Cannot lower `xmap` with ordered effects.')
  tiled_outs, _ = mlir.jaxpr_subcomp(sub_ctx, vectorized_jaxpr, mlir.TokenSet(),
                                     const_nodes, *tiled_ins,
                                     dim_var_values=ctx.dim_var_values)

  outs = [
      mlir.lower_fun(
          partial(_untile, out_axes=ans_out_axes, axis_sizes=local_mesh_shape,
                  platform=ctx.module_context.platform),
          multiple_results=False)(
              ctx.replace(primitive=None,
                          avals_in=[vectorized_outvar.aval],
                          avals_out=None), tiled_out)[0]
      for v, vectorized_outvar, tiled_out, ans_out_axes
      in zip(call_jaxpr.outvars, vectorized_jaxpr.outvars, tiled_outs,
             mesh_out_axes)]
  return outs
