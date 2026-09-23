def _or_lowering_rule(ctx: LoweringRuleContext, lhs, rhs):
  return arith.OrIOp(lhs, rhs).result
