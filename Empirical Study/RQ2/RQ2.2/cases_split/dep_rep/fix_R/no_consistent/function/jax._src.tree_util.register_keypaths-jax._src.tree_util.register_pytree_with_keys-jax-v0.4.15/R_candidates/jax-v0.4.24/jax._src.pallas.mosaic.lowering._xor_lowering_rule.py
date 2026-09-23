def _xor_lowering_rule(ctx: LoweringRuleContext, x, y):
  return arith.XOrIOp(x, y).result
