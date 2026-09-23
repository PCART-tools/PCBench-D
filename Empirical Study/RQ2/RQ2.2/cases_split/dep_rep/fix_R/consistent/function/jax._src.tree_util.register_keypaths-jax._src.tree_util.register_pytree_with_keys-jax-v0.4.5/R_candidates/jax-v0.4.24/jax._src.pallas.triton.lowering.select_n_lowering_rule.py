def select_n_lowering_rule(ctx: TritonLoweringRuleContext, pred, a, b):
  return tc.semantic.where(pred, b, a)
