def dilate_dim(d: DimSize, dilation: DimSize) -> DimSize:
  """Implements `0 if d == 0 else 1 + dilation * (d - 1))`"""
  handler, ds = _dim_handler_and_canonical(d, dilation)
  return handler.dilate(*ds)
