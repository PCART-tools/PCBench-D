def _max_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return tc.math.max(a, b)
