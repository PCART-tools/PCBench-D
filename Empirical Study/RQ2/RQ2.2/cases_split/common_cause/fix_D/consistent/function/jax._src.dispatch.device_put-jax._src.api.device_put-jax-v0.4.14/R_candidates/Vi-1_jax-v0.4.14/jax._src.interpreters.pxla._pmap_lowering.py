def _pmap_lowering(ctx, *in_nodes, axis_name,
                   axis_size, global_axis_size, devices, name,
                   call_jaxpr, backend=None, in_axes, out_axes,
                   donated_invars, is_explicit_global_axis_size):
  del donated_invars  # Unused.
  xla.check_backend_matches(backend, ctx.module_context.platform)
  # We in-line here rather than generating a Call HLO as in the xla_call
  # translation rule just because the extra tuple stuff is a pain.
  if ctx.module_context.axis_env.names and devices is not None:
    raise ValueError("Nested pmap with explicit devices argument.")
  new_env = xla.extend_axis_env(ctx.module_context.axis_env, axis_name,
                                global_axis_size)
  # Shard the in_nodes that are mapped
  in_avals = [v.aval for v in call_jaxpr.invars]
  in_nodes_sharded = (
    _hlo_shard(aval, new_env, mlir.wrap_singleton_ir_values(in_node), in_axis)
    if in_axis is not None else mlir.wrap_singleton_ir_values(in_node)
    for aval, in_node, in_axis in zip(in_avals, in_nodes, in_axes))

  with maybe_extend_axis_env(axis_name, global_axis_size, None):  # type: ignore
    sub_ctx = ctx.module_context.replace(
        axis_context=sharding_impls.ReplicaAxisContext(new_env),
        name_stack=ctx.module_context.name_stack.extend(
            util.wrap_name(name, 'pmap')))
    sharded_outs, _ = mlir.jaxpr_subcomp(sub_ctx, call_jaxpr, mlir.TokenSet(), (),
                                         *in_nodes_sharded,
                                         dim_var_values=ctx.dim_var_values)
  out_avals = [v.aval for v in call_jaxpr.outvars]
  outs = [_hlo_unshard(ctx, aval, new_env, out_axis, shard,
                        platform=ctx.module_context.platform)
          for aval, out_axis, shard in zip(out_avals, out_axes, sharded_outs)]
  return outs
