def sum_dim(*ds: DimSize) -> DimSize:
  handler, ds = _dim_handler_and_canonical(*ds)
  return handler.sum(*ds)
