def _broadcast_in_dim_lowering_rule(
    ctx: TritonLoweringRuleContext, a, *, broadcast_dimensions, shape
):
  if not a.type.is_block():
    return tc.broadcast_to(a, shape)
  expand_dims = [i for i in range(len(shape)) if i not in broadcast_dimensions]
  for dim in expand_dims:
    a = tc.expand_dims(a, dim)
  return tc.broadcast_to(a, shape)
