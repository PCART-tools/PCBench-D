def select_n_lowering_rule(ctx: TritonLoweringRuleContext, pred, a, b):
  return tl.semantic.where(pred, b, a, ctx.builder)
