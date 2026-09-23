@_wraps(np.dtype)
def _jnp_dtype(obj, align=False, copy=False):
  """Similar to np.dtype, but respects JAX dtype defaults."""
  if obj is None:
    obj = dtypes.float_
  elif isinstance(obj, type) and obj in dtypes.python_scalar_dtypes:
    obj = _DEFAULT_TYPEMAP[np.dtype(obj, align=align, copy=copy).type]
  return np.dtype(obj, align=align, copy=copy)
