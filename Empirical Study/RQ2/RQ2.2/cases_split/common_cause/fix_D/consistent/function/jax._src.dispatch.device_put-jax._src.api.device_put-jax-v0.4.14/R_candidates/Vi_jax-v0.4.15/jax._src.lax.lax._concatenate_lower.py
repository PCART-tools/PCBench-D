def _concatenate_lower(ctx, *xs, dimension):
  return hlo.ConcatenateOp(xs, mlir.i64_attr(dimension)).results
