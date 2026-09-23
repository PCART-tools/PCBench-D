def num_float_bits(dtype):
  return _dtypes.finfo(_dtypes.canonicalize_dtype(dtype)).bits
