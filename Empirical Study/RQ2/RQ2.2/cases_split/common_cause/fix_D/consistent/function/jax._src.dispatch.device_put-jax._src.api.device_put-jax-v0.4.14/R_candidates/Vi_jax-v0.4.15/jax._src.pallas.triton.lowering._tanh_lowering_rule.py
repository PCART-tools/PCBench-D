def _tanh_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.math.tanh(a, _builder=ctx.builder)
