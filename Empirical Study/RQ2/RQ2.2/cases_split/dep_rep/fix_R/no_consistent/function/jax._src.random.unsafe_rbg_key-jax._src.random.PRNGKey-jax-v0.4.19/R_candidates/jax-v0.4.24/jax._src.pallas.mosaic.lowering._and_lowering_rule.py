def _and_lowering_rule(ctx: LoweringRuleContext, lhs, rhs):
  return arith.AndIOp(lhs, rhs).result
