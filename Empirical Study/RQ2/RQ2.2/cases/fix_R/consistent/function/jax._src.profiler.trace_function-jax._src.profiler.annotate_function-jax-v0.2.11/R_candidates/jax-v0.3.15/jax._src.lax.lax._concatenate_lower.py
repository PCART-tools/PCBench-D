def _concatenate_lower(ctx, *xs, dimension):
  return mhlo.ConcatenateOp(xs, mlir.i64_attr(dimension)).results
