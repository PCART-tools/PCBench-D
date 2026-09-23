@util.implements(np.dtype)
def _jnp_dtype(obj: DTypeLike | None, *, align: bool = False,
               copy: bool = False) -> DType:
  """Similar to np.dtype, but respects JAX dtype defaults."""
  if dtypes.issubdtype(obj, dtypes.extended):
    return obj  # type: ignore[return-value]
  if obj is None:
    obj = dtypes.float_
  elif isinstance(obj, type) and obj in dtypes.python_scalar_dtypes:
    obj = _DEFAULT_TYPEMAP[obj]
  return np.dtype(obj, align=align, copy=copy)
