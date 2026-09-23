def issubdtype(a: DTypeLike, b: DTypeLike) -> bool:
  """Returns True if first argument is a typecode lower/equal in type hierarchy.

  This is like :func:`numpy.issubdtype`, but can handle dtype extensions such as
  :obj:`jax.dtypes.bfloat16`.
  '"""
  if _fp8_enabled:
    if a == "float8_e4m3fn":
      a = float8_e4m3fn
    if a == float8_e4m3fn:
      if isinstance(b, np.dtype):
        return b == _float8_e4m3fn_dtype
      else:
        return b in [float8_e4m3fn, np.floating, np.inexact, np.number]
    if a == "float8_e5m2":
      a = float8_e5m2
    if a == float8_e5m2:
      if isinstance(b, np.dtype):
        return b == _float8_e5m2_dtype
      else:
        return b in [float8_e5m2, np.floating, np.inexact, np.number]
  if a == "bfloat16":
    a = bfloat16
  if a == bfloat16:
    if isinstance(b, np.dtype):
      return b == _bfloat16_dtype
    else:
      return b in [bfloat16, np.floating, np.inexact, np.number]
  if not _issubclass(b, np.generic):
    # Workaround for JAX scalar types. NumPy's issubdtype has a backward
    # compatibility behavior for the second argument of issubdtype that
    # interacts badly with JAX's custom scalar types. As a workaround,
    # explicitly cast the second argument to a NumPy type object.
    b = np.dtype(b).type
  try:
    return np.issubdtype(a, b)
  except TypeError:  # e.g. if 'a' is not a np.dtype
    return False
