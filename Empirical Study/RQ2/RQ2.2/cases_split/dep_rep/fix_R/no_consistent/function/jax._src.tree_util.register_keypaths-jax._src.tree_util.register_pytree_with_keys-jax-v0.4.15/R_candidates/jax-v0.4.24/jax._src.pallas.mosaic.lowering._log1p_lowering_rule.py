def _log1p_lowering_rule(ctx: LoweringRuleContext, x):
  return math.Log1pOp(x).result
