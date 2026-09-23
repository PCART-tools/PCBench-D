def _sin_lowering_rule(ctx: LoweringRuleContext, x):
  return math.SinOp(x).result
