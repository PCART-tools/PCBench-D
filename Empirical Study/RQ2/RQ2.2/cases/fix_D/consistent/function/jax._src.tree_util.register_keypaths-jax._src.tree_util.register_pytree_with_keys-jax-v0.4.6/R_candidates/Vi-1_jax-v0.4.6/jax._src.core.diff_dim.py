def diff_dim(d1: DimSize, d2: DimSize) -> DimSize:
  handler, ds = _dim_handler_and_canonical(d1, d2)
  return handler.diff(*ds)
