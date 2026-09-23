def _atomic_cas_lowering_rule(ctx: TritonLoweringRuleContext, ptr, cmp, val):
  return tl.atomic_cas(ptr, cmp, val, _builder=ctx.builder)
