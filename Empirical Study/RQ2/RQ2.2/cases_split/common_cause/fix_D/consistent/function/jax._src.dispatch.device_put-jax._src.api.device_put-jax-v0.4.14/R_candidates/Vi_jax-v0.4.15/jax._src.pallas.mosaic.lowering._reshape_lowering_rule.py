def _reshape_lowering_rule(ctx: LoweringRuleContext, x, new_sizes, dimensions):
  if dimensions is not None:
    raise NotImplementedError
  if any(d is None for d in new_sizes):
    raise NotImplementedError
  return vector.ShapeCastOp(aval_to_ir_type(ctx.avals_out[0]), x).result
