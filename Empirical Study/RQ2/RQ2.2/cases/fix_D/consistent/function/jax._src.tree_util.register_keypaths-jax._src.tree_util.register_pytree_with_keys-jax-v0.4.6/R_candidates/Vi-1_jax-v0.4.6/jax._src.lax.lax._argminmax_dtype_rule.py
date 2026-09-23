def _argminmax_dtype_rule(operand, *, axes, index_dtype):
  if not dtypes.issubdtype(index_dtype, np.integer):
    raise TypeError("index_dtype must be an integer type, but got {}"
                    .format(np.dtype(index_dtype).name))
  return index_dtype
