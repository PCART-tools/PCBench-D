def _reshape_lower(ctx, x, *dyn_shape, new_sizes, dimensions):
  aval_out, = ctx.avals_out
  if dimensions is not None:
    x = hlo.transpose(x, mlir.dense_int_array(dimensions))
  if dyn_shape:
    aval_out = aval_out.update(shape=_merge_dyn_shape(new_sizes, dyn_shape))
  return [mlir.reshape(ctx, x, aval_out)]
