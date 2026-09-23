def issubdtype(a: DTypeLike | None, b: DTypeLike | None) -> bool:
  """Returns True if first argument is a typecode lower/equal in type hierarchy.

  This is like :func:`numpy.issubdtype`, but can handle dtype extensions such as
  :obj:`jax.dtypes.bfloat16` and `jax.dtypes.prng_key`.
  """
  # Main departures from np.issubdtype are:
  # - "extended" dtypes (like prng key types) are not normal numpy dtypes, so we
  #   need to handle them specifically. However, their scalar types do conform to
  #   the numpy scalar type hierarchy.
  # - custom dtypes (like bfloat16, int4, etc.) are normal numpy dtypes, but they
  #   don't conform to the standard numpy type hierarchy (e.g. the bfloat16 scalar
  #   type is not a subclass of np.floating) so we must also handle these specially.

  # First handle extended dtypes. This is important for performance because
  # isinstance(x, extended) is called frequently within JAX internals.
  if _issubclass(b, extended):
    if isinstance(a, ExtendedDType):
      return _issubclass(a.type, b)
    if _issubclass(a, np.generic):
      return _issubclass(a, b)
    return _issubclass(np.dtype(a).type, b)
  if isinstance(b, ExtendedDType):
    return isinstance(a, ExtendedDType) and a == b
  if isinstance(a, ExtendedDType):
    a = a.type

  # For all others, normalize inputs to scalar types.
  a_sctype = a if _issubclass(a, np.generic) else np.dtype(a).type
  b_sctype = b if _issubclass(b, np.generic) else np.dtype(b).type

  # Now do special handling of custom float and int types, as they don't conform
  # to the normal scalar type hierarchy.
  if a_sctype in _custom_float_scalar_types:
    return b_sctype in {a_sctype, np.floating, np.inexact, np.number, np.generic}
  if a_sctype == int4:
    return b_sctype in {a_sctype, np.signedinteger, np.integer, np.number, np.generic}
  if a_sctype == uint4:
    return b_sctype in {a_sctype, np.unsignedinteger, np.integer, np.number, np.generic}

  # Otherwise, fall back to numpy.issubdtype
  return np.issubdtype(a_sctype, b_sctype)
