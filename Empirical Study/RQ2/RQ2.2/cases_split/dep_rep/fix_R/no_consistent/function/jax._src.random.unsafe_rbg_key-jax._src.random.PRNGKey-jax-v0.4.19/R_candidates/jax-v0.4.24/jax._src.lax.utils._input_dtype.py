def _input_dtype(x, *_, **__):
  return dtypes.canonicalize_dtype(x.dtype, allow_extended_dtype=True)
