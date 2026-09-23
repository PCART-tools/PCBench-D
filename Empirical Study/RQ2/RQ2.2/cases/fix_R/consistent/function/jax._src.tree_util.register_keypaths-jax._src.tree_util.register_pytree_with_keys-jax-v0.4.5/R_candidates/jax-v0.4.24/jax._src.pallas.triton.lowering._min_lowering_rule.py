def _min_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return tc.math.min(a, b)
