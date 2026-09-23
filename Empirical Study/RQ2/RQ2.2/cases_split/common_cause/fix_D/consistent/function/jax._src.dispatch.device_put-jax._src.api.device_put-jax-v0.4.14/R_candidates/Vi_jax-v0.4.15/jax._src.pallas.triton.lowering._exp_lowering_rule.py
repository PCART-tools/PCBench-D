def _exp_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.exp(a, _builder=ctx.builder)
