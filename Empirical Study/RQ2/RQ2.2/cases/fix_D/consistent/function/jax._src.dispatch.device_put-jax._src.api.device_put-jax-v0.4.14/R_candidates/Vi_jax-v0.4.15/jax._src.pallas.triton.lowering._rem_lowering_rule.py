def _rem_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__mod__(b, _builder=ctx.builder)
