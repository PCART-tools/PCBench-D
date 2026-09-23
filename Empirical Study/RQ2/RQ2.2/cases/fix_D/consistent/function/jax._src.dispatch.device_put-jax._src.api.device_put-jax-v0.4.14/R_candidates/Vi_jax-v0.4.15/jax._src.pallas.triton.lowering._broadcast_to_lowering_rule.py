def _broadcast_to_lowering_rule(
    ctx: TritonLoweringRuleContext, a, *, shape
):
  shape = map(tl.constexpr, shape)
  return tl.broadcast_to(a, shape, _builder=ctx.builder)
