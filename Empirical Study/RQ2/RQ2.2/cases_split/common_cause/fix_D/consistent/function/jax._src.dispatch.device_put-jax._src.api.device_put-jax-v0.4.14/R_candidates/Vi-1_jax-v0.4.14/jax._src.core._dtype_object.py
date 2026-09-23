def _dtype_object(dtype):
  return dtype if dtypes.issubdtype(dtype, dtypes.extended) else np.dtype(dtype)
