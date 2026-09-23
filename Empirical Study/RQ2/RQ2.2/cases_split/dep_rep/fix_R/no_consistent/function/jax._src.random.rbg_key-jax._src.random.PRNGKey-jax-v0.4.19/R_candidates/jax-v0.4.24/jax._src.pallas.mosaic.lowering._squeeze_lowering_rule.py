def _squeeze_lowering_rule(ctx: LoweringRuleContext, x, dimensions):
  del dimensions  # Unused.
  (aval_in,) = ctx.avals_in
  (aval_out,) = ctx.avals_out
  if not aval_out.shape:
    return vector.ExtractOp(x, [], [0] * len(aval_in.shape)).result
  return vector.ShapeCastOp(aval_to_ir_type(ctx.avals_out[0]), x).result
