def eq_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__eq__(b, _builder=ctx.builder)
