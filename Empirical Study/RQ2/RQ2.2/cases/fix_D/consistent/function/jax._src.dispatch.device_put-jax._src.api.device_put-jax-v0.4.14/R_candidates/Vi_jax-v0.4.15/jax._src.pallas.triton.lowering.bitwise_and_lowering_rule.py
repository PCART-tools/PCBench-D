def bitwise_and_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__and__(b, _builder=ctx.builder)
