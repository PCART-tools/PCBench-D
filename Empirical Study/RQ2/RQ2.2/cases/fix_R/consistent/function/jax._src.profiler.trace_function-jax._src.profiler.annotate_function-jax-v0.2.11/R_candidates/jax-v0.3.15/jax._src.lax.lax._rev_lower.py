def _rev_lower(ctx, x, *, dimensions):
  return mhlo.ReverseOp(x, mlir.dense_int_elements(dimensions)).results
