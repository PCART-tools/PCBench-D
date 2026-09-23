def _reshape_lowering_rule(
    ctx: TritonLoweringRuleContext, a, *, new_sizes, dimensions
):
  del new_sizes, dimensions
  # Short-circuit to avoid unneeded reshape.
  dst_shp = ctx.avals_out[0].shape
  if tuple(s.value for s in a.shape) == dst_shp:
    return a
  if not a.type.is_block():
    if dst_shp:
      return tl.broadcast_to(a, [tl.constexpr(s) for s in dst_shp],
                             _builder=ctx.builder)
    return a
  # Expand-dims or reduce-sum to handle singleton dims.
  if ([s.value for s in a.shape if s.value != 1] ==
      [s for s in dst_shp if s != 1]):
    # Eliminate one difference and recurse.
    for i in range(max(len(a.shape), len(dst_shp))):
      if (i < len(a.shape) and i < len(dst_shp) and
          a.shape[i].value == dst_shp[i]):
        continue
      # Use expand_dims to add a singleton dim.
      if i < len(dst_shp) and dst_shp[i] == 1:
        return _reshape_lowering_rule(
            ctx, tl.semantic.expand_dims(a, i, builder=ctx.builder),
            new_sizes=None, dimensions=None)
      # Use a reduction to eliminate singleton dim.
      if a.shape[i].value == 1:
        reduce_ctx = ctx.replace(
            avals_in=[ctx.avals_in[0].update(
                shape=tuple(d.value for d in a.shape))],
            avals_out=[ctx.avals_in[0].update(
                shape=tuple(d.value for di, d in enumerate(a.shape)
                            if di != i))])
        return _reshape_lowering_rule(
            ctx,
            _reduce_lowering(jnp.add, reduce_ctx, a, axes=(i,)),
            new_sizes=None, dimensions=None)

  shape = [tl.constexpr(s) for s in dst_shp]
  return tl.reshape(a, shape, _builder=ctx.builder)
