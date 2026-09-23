def _abs_lowering_rule(ctx: TritonLoweringRuleContext, x):
  return tl.abs(x, _builder=ctx.builder)
