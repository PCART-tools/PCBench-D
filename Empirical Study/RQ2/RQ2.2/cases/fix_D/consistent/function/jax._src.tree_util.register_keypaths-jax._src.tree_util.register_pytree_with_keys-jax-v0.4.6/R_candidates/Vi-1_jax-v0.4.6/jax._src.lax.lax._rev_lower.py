def _rev_lower(ctx, x, *, dimensions):
  return hlo.ReverseOp(x, mlir.dense_int_elements(dimensions)).results
