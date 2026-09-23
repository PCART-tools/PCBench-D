def _sub_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__sub__(b, _builder=ctx.builder)
