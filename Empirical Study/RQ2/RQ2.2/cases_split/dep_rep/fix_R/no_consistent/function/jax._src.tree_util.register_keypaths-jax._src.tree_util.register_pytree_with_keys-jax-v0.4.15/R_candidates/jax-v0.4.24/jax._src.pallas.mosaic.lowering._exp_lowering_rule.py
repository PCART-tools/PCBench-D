def _exp_lowering_rule(ctx: LoweringRuleContext, x):
  return math.ExpOp(x).result
