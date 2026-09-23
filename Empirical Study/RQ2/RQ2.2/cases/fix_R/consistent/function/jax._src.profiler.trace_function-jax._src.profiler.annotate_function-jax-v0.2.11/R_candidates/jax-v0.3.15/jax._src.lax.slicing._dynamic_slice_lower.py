def _dynamic_slice_lower(ctx, x, *start_indices, slice_sizes):
  return mhlo.DynamicSliceOp(x, start_indices,
                             mlir.dense_int_elements(slice_sizes)).results
