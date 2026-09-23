def _get_min_identity(dtype):
  if dtypes.issubdtype(dtype, np.inexact):
    return np.array(np.inf, dtype)
  elif dtypes.issubdtype(dtype, np.integer):
    return np.array(dtypes.iinfo(dtype).max, dtype)
  elif dtypes.issubdtype(dtype, np.bool_):
    return np.array(True, np.bool_)
