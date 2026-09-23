def _dtype(x: Any) -> DType:
  return dtypes.dtype(x, canonicalize=True)
