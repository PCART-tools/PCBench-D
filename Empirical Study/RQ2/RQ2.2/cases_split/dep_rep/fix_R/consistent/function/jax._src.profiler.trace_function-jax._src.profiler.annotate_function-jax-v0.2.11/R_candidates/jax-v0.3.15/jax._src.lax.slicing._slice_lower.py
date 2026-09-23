def _slice_lower(ctx, x, *, start_indices, limit_indices, strides):
  strides = strides or [1] * len(start_indices)
  return mhlo.SliceOp(x,
                      mlir.dense_int_elements(start_indices),
                      mlir.dense_int_elements(limit_indices),
                      mlir.dense_int_elements(strides)).results
