def _neg_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return a.__neg__(_builder=ctx.builder)
