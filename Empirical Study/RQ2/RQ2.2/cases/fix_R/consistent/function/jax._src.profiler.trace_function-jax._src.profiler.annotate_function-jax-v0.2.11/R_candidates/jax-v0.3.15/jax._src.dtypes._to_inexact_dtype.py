def _to_inexact_dtype(dtype):
  """Promotes a dtype into an inexact dtype, if it is not already one."""
  dtype = np.dtype(dtype)
  return _dtype_to_inexact.get(dtype, dtype)
