def _gt_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  return a.__gt__(b, _builder=ctx.builder)
