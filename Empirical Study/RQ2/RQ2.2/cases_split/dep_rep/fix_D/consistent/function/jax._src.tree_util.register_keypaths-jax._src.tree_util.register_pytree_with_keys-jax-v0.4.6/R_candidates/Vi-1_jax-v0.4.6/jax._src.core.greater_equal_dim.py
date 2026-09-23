def greater_equal_dim(d1: DimSize, d2: DimSize) -> bool:
  handler, ds = _dim_handler_and_canonical(d1, d2)
  return handler.symbolic_equal(*ds) or handler.greater_equal(*ds)
