def _add_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__add__(b, _builder=ctx.builder)
