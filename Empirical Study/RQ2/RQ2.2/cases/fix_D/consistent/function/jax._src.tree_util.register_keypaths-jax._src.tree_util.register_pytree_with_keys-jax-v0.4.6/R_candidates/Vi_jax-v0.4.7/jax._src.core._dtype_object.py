def _dtype_object(dtype):
  return dtype if type(dtype) in opaque_dtypes else np.dtype(dtype)
