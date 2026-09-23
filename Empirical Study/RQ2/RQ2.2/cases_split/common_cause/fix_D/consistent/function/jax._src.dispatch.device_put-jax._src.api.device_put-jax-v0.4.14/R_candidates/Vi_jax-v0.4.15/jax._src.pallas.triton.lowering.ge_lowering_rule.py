def ge_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__ge__(b, _builder=ctx.builder)
