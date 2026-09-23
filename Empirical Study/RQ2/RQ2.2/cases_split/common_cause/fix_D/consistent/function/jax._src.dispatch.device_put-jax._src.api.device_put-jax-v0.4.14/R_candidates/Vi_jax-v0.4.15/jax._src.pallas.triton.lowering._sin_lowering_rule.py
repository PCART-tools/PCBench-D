def _sin_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.sin(a, _builder=ctx.builder)
