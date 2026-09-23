def _slice_lower(ctx, x, *, start_indices, limit_indices, strides):
  strides = strides or [1] * len(start_indices)
  aval_out, = ctx.avals_out
  return [mlir.slice_op(ctx, x, aval_out,
                        start_indices=start_indices, limit_indices=limit_indices, strides=strides)]
