def stride_dim(d: DimSize, window_size: DimSize, window_stride: DimSize) -> DimSize:
  handler, ds = _dim_handler_and_canonical(d, window_size, window_stride)
  return handler.stride(*ds)
