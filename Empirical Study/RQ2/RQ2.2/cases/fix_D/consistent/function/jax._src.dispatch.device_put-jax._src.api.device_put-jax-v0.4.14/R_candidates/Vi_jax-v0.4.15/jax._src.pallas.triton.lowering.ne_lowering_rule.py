def ne_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__ne__(b, _builder=ctx.builder)
