def issubdtype(a: DTypeLike, b: DTypeLike) -> bool:
  """Returns True if first argument is a typecode lower/equal in type hierarchy.

  This is like :func:`numpy.issubdtype`, but can handle dtype extensions such as
  :obj:`jax.dtypes.bfloat16`.
  """
  if isinstance(a, ExtendedDType):
    return _issubclass(a.type, b)
  elif _issubclass(b, extended):
    return False
  # Canonicalizes all concrete types to np.dtype instances
  a = a if _is_typeclass(a) else np.dtype(a)
  b = b if _is_typeclass(b) else np.dtype(b)
  if isinstance(a, np.dtype):
    if a in _custom_float_dtypes:
      # Avoid implicitly casting list elements below to a dtype.
      if isinstance(b, np.dtype):
        return a == b
      return b in [np.floating, np.inexact, np.number]
    if a == _int4_dtype:
      if isinstance(b, np.dtype):
        return a == b
      return b in [np.signedinteger, np.integer, np.number]
    if a == _uint4_dtype:
      if isinstance(b, np.dtype):
        return a == b
      return b in [np.unsignedinteger, np.integer, np.number]
  return np.issubdtype(a, b)
