def bitwise_or_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__or__(b, _builder=ctx.builder)
