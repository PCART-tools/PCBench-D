def _rsqrt_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.math.rsqrt(a, _builder=ctx.builder)
