def _sqrt_lowering_rule(ctx: LoweringRuleContext, x):
  return math.SqrtOp(x).result
