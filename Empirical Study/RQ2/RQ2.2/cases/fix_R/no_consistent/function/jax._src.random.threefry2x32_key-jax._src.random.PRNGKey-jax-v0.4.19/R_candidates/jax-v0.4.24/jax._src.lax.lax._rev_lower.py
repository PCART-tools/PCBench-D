def _rev_lower(ctx, x, *, dimensions):
  return [hlo.reverse(x, mlir.dense_int_array(dimensions))]
