def _bitcast_convert_type_dtype_rule(operand, *, new_dtype):
  old_dtype = dtypes.canonicalize_dtype(operand.dtype)
  if dtypes.issubdtype(old_dtype, np.bool_) or dtypes.issubdtype(old_dtype, np.complexfloating):
    if old_dtype != new_dtype:
      raise TypeError(f"`bitcast_convert_type` for operand type ({old_dtype}) cannot have different destination type ({new_dtype})")
  if np.dtype(old_dtype).itemsize != np.dtype(new_dtype).itemsize:
    raise TypeError(f"`bitcast_convert_type` for operand type ({old_dtype}) must have destination type ({new_dtype}) of same size.")
  return new_dtype
