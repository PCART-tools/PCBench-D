def _iota_lowering_rule(
    ctx: TritonLoweringRuleContext, *, dtype, shape, dimension
):
  if dimension != 0:
    raise NotImplementedError()
  return tl.arange(0, shape[0], _builder=ctx.builder)
