def _reshape_lowering_rule(
    ctx: TritonLoweringRuleContext, a, *, new_sizes, dimensions
):
  del new_sizes  # Unused.
  if dimensions is not None:
    return ValueError("`dimensions` is not supported.")

  dst_shape = ctx.avals_out[0].shape
  if not a.type.is_block():
    assert all(dim_size == 1 for dim_size in dst_shape)
    return tc.broadcast_to(a, dst_shape)

  # Expand-dims or reduce-sum to handle singleton dims as `tl.reshape` is not
  # currently implemented.
  i = 0
  while a.shape != dst_shape:
    dim_size = a.shape[i] if i < len(a.shape) else None
    dst_dim_size = dst_shape[i] if i < len(dst_shape) else None
    if dim_size == dst_dim_size:
      i += 1
    elif dst_dim_size == 1:
      a = tc.expand_dims(a, axis=i)
      i += 1
    elif dim_size == 1:
      in_shape = a.shape
      out_shape = tuple(d for di, d in enumerate(a.shape) if di != i)
      reduce_ctx = ctx.replace(
          avals_in=[ctx.avals_in[0].update(shape=in_shape)],
          avals_out=[ctx.avals_in[0].update(shape=out_shape)],
      )
      a = _reduce_lowering(jnp.add, reduce_ctx, a, axes=(i,))
    else:  # We expect this to fail.
      return tc.reshape(a, dst_shape)
  return a
