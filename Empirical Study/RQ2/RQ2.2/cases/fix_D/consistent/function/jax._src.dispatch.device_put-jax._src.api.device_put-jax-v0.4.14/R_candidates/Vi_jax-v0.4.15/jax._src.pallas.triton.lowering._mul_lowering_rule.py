def _mul_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__mul__(b, _builder=ctx.builder)
