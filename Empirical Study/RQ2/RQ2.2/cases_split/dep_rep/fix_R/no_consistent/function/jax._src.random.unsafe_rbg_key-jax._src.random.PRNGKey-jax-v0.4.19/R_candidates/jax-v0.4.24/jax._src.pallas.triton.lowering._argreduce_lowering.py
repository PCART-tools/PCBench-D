def _argreduce_lowering(
    body, ctx: TritonLoweringRuleContext, a, *, axes, index_dtype
):
  if index_dtype != jnp.int32:
    raise ValueError("`index_type` must be i32.")
  if len(axes) != 1:
    raise ValueError("`pallas` reduce operations only support one reduce axis.")
  (axis,) = axes
  n = ctx.avals_in[0].shape[axis]
  index = tc.arange(0, n)
  if len(a.shape) > 1:
    # Broadcast index across the non-reduced axes
    for i in range(len(a.shape)):
      if i != axis:
        index = tc.expand_dims(index, i)
    index = tc.broadcast_to(index, a.shape)
  ctx = ctx.replace(
      avals_in=[
          ctx.avals_in[0],
          ctx.avals_in[0].update(dtype=jnp.dtype("int32")),
      ]
  )
  _, indices = _reduction_lowering(body, ctx, (a, index), axes=axes)
  return indices
