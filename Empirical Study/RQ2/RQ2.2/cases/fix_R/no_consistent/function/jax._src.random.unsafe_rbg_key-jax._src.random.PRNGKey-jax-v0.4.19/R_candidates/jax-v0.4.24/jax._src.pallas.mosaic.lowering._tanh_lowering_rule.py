def _tanh_lowering_rule(ctx: LoweringRuleContext, x):
  return math.TanhOp(x).result
