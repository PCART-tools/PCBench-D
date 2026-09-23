def _bitcast_convert_type_shape_rule(operand, *, new_dtype):
  old_dtype = dtypes.canonicalize_dtype(operand.dtype)
  new_dtype = dtypes.canonicalize_dtype(new_dtype)

  if old_dtype.itemsize == new_dtype.itemsize:
    return operand.shape
  elif old_dtype.itemsize > new_dtype.itemsize:
    return (*operand.shape, old_dtype.itemsize // new_dtype.itemsize)
  else:
    dim_size = operand.shape[-1] if operand.shape else 1
    if dim_size * old_dtype.itemsize != new_dtype.itemsize:
      raise ValueError(
        f"Attempting to convert array of shape {operand.shape} "
        f"from {str(old_dtype)} of size {old_dtype.itemsize} "
        f"to {str(new_dtype)} of size {new_dtype.itemsize}, "
        f"but {dim_size} * {old_dtype.itemsize} != {new_dtype.itemsize}")
    return operand.shape[:-1]
