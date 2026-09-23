def _argreduce_lowering(
    body, ctx: TritonLoweringRuleContext, a, *, axes, index_dtype
):
  if index_dtype != jnp.int32:
    raise ValueError("`index_type` must be f32.")
  if len(axes) != 1:
    raise ValueError("`pallas` reduce operations only support one reduce axis.")
  (axis,) = axes
  n = ctx.avals_in[0].shape[axis]
  index = tl.arange(0, n, _builder=ctx.builder)
  if len(a.shape) > 1:
    # Broadcast index across the non-reduced axes
    expand_dims_index = [tl.constexpr(None)] * len(a.shape)
    expand_dims_index[axis] = slice(None)
    index = index.__getitem__(expand_dims_index, _builder=ctx.builder)
    index = tl.core.broadcast_to(index, a.shape, _builder=ctx.builder)
  ctx = ctx.replace(
      avals_in=[
          ctx.avals_in[0],
          ctx.avals_in[0].update(dtype=jnp.dtype("int32")),
      ]
  )
  _, indices = _reduction_lowering(body, ctx, (a, index), axes=axes)
  return indices
