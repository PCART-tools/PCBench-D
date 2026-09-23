def _cumsum_lowering_rule(
    ctx: TritonLoweringRuleContext,
    x,
    *, axis: int, reverse: bool
):
  if reverse:
    raise NotImplementedError("Reverse cumsum is not supported.")
  return _associative_scan_lowering(jnp.add, ctx, x, (axis,))[0]
