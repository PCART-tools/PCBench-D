def _shift_right_logical_lowering_rules(ctx: LoweringRuleContext, x, d):
  return arith.ShRUIOp(x, d).result
