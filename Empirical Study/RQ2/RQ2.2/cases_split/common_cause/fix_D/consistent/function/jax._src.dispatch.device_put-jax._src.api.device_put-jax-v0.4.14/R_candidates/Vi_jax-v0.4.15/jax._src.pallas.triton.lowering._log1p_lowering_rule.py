def _log1p_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.math.log1p(a, _builder=ctx.builder)
