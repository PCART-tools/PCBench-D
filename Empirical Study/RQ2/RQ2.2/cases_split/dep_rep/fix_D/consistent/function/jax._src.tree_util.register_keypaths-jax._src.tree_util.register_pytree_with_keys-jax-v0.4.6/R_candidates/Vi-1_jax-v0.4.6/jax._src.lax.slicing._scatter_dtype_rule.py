def _scatter_dtype_rule(operand, indices, updates, **kwargs):
  if not dtypes.issubdtype(indices.dtype, np.integer):
    raise ValueError("indices must have an integer type")
  lax._check_same_dtypes("scatter", False, operand.dtype, updates.dtype)
  return dtypes.canonicalize_dtype(operand.dtype)
