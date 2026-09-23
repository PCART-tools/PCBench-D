def _concatenate_lower(ctx, *xs, dimension):
  return [hlo.concatenate(xs, mlir.i64_attr(dimension))]
