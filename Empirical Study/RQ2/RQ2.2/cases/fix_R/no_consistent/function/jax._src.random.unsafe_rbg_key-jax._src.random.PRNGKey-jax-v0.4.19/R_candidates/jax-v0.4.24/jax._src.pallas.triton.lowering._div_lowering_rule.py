def _div_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  [out_aval] = ctx.avals_out
  a = tc.broadcast_to(a, out_aval.shape)
  b = tc.broadcast_to(b, out_aval.shape)
  if a.dtype.is_floating() or b.dtype.is_floating():
    return tc.semantic.truediv(a, b)
  return tc.semantic.floordiv(a, b)
