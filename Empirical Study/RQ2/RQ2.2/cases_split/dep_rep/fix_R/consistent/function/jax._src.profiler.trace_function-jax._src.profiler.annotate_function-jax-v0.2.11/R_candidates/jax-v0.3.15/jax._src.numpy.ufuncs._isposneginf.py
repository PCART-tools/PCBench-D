def _isposneginf(infinity, x, out):
  if out is not None:
    raise NotImplementedError("The 'out' argument to isneginf/isposinf is not supported.")
  dtype = dtypes.dtype(x)
  if dtypes.issubdtype(dtype, np.floating):
    return lax.eq(x, _constant_like(x, infinity))
  elif dtypes.issubdtype(dtype, np.complexfloating):
    raise ValueError("isposinf/isneginf are not well defined for complex types")
  else:
    return lax.full_like(x, False, dtype=np.bool_)
