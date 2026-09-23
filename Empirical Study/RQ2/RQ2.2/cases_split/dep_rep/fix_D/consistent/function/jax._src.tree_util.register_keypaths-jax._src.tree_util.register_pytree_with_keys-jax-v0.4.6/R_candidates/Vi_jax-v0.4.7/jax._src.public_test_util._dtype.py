def _dtype(x):
  if hasattr(x, 'dtype'):
    return x.dtype
  elif type(x) in _dtypes.python_scalar_dtypes:
    return np.dtype(_dtypes.python_scalar_dtypes[type(x)])
  else:
    return np.asarray(x).dtype
