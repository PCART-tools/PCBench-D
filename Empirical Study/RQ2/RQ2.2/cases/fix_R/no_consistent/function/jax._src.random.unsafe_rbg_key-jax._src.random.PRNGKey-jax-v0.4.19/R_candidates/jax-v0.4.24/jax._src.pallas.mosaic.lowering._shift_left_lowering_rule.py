def _shift_left_lowering_rule(ctx: LoweringRuleContext, x, d):
  return arith.ShLIOp(x, d).result
