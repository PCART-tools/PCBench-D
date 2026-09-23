def _broadcast_in_dim_lowering_rule(
    ctx: TritonLoweringRuleContext, a, *, broadcast_dimensions, shape
):
  shape = map(tl.constexpr, shape)
  if not a.type.is_block():
    return tl.broadcast_to(a, shape, _builder=ctx.builder)
  expand_dims = [i for i in range(len(shape)) if i not in broadcast_dimensions]
  for dim in expand_dims:
    a = tl.semantic.expand_dims(a, dim, ctx.builder)
  return tl.broadcast_to(a, shape, _builder=ctx.builder)
