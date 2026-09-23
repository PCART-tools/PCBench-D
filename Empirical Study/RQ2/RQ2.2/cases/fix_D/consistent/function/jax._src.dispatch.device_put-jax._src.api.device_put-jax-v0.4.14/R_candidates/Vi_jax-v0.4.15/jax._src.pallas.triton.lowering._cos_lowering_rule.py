def _cos_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.cos(a, _builder=ctx.builder)
