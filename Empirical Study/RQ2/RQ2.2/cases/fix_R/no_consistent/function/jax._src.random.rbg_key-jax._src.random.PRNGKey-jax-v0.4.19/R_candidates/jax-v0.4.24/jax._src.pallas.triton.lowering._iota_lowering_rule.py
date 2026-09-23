def _iota_lowering_rule(
    ctx: TritonLoweringRuleContext, *, dtype, shape, dimension
):
  if dimension != 0:
    raise NotImplementedError()
  return tc.arange(0, shape[0])
