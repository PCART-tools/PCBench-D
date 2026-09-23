def _sqrt_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.sqrt(a, _builder=ctx.builder)
