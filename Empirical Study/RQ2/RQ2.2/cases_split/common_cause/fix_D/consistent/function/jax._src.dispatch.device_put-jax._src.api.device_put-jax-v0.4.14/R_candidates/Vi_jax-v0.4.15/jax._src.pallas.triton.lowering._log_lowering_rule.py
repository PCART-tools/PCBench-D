def _log_lowering_rule(ctx: TritonLoweringRuleContext, a):
  return tl.log(a, _builder=ctx.builder)
