def _cond_lowering_rule(ctx: LoweringRuleContext, *args, branches, linear):
  index, *args = args
  out_types = map(aval_to_ir_type, ctx.avals_out)
  pred = arith.CmpIOp(
      arith.CmpIPredicate.ne, index, ir_constant(0, index.type)
  ).result
  if_op = scf.IfOp(pred, out_types, hasElse=True)
  lowering_context = ctx.lowering_context.replace(
      block_shapes=ctx.block_shapes[1:],
  )
  with ir.InsertionPoint(if_op.then_block):
    # TODO(b/300272065): Use `scf.IndexSwitchOp` instead of a cascade of
    # if/else.
    if len(branches) > 2:
      out = _cond_lowering_rule(
          ctx,
          arith.SubIOp(index, ir_constant(1, index.type)).result,
          *args,
          branches=branches[1:],
          linear=linear,
      )
    else:
      out = jaxpr_subcomp(lowering_context, branches[1].jaxpr, *args)
    scf.YieldOp(out)
  with ir.InsertionPoint(if_op.else_block):
    out = jaxpr_subcomp(lowering_context, branches[0].jaxpr, *args)
    scf.YieldOp(out)
  return if_op.results
