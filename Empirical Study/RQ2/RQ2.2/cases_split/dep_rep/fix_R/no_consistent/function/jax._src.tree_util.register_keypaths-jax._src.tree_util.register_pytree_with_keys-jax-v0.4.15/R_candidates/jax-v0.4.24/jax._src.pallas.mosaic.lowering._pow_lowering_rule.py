def _pow_lowering_rule(ctx: LoweringRuleContext, x, y):
  if not isinstance(x, ir.Value) and x == 2.:
    return math.Exp2Op(y).result
  x, y = _bcast(x, y, ctx.avals_in[0], ctx.avals_in[1], ctx.avals_out[0])
  return math.PowFOp(x, y).result
