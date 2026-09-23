def _cond_lowering_rule(ctx: LoweringRuleContext, *args, branches, linear):
  del linear
  if len(branches) > 2:
    raise NotImplementedError
  pred, *args = args
  out_types = map(aval_to_ir_type, ctx.avals_out)
  pred = arith.TruncIOp(
      aval_to_ir_type(jax_core.ShapedArray((), jnp.bool_)), pred
  ).result
  # Specialize to singleton `if`s
  singleton = len(out_types) == 1
  if singleton:
    out_types = out_types[0]
  if_op = scf.IfOp(pred, out_types, hasElse=True)
  lowering_context = ctx.lowering_context.replace(
      block_shapes=ctx.block_shapes[1:],
  )
  with ir.InsertionPoint(if_op.then_block):
    out = jaxpr_subcomp(lowering_context, branches[1].jaxpr, *args)
    scf.YieldOp(out)
  with ir.InsertionPoint(if_op.else_block):
    out = jaxpr_subcomp(lowering_context, branches[0].jaxpr, *args)
    scf.YieldOp(out)
  if singleton:
    return if_op.result
  return if_op.results
