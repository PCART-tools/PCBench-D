def _log_lowering_rule(ctx: LoweringRuleContext, x):
  return math.LogOp(x).result
