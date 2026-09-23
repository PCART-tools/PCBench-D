def _pow_lowering_rule(ctx: TritonLoweringRuleContext, a, y):
  return tl.math.pow(a, y, _builder=ctx.builder)
