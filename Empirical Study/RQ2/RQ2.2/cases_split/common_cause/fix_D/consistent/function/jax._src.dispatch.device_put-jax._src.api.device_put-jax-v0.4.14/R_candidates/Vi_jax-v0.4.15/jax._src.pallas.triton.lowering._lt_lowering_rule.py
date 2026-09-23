def _lt_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__lt__(b, _builder=ctx.builder)
