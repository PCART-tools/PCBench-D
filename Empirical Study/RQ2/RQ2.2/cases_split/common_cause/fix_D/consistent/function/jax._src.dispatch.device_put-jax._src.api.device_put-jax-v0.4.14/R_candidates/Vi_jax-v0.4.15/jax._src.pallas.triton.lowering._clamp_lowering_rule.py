def _clamp_lowering_rule(ctx: TritonLoweringRuleContext, min, operand, max):
  return _min_lowering_rule(ctx, max_lowering_rule(ctx, min, operand), max)
