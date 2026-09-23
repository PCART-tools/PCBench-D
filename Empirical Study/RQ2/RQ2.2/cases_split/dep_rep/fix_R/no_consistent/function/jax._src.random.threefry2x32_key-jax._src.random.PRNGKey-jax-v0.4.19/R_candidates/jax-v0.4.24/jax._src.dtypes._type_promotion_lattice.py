def _type_promotion_lattice(jax_numpy_dtype_promotion: str) -> dict[JAXType, list[JAXType]]:
  """
  Return the type promotion lattice in the form of a DAG.
  This DAG maps each type to its immediately higher type on the lattice.
  """
  b1, = _bool_types
  if int4 is not None:
    _uint4, u1, u2, u4, u8, _int4, i1, i2, i4, i8 = _int_types  # pytype: disable=bad-unpacking
  else:
    u1, u2, u4, u8, i1, i2, i4, i8 = _int_types  # pytype: disable=bad-unpacking
  *f1_types, bf, f2, f4, f8 = _float_types
  c4, c8 = _complex_types
  i_, f_, c_ = _weak_types
  if jax_numpy_dtype_promotion == 'standard':
    out: dict[JAXType, list[JAXType]]
    out = {
      b1: [i_],
      u1: [i2, u2], u2: [i4, u4], u4: [i8, u8], u8: [f_],
      i_: [u1, i1], i1: [i2], i2: [i4], i4: [i8], i8: [f_],
      f_: [*f1_types, bf, f2, c_],
      **{t: [] for t in f1_types}, bf: [f4], f2: [f4], f4: [f8, c4], f8: [c8],
      c_: [c4], c4: [c8], c8: [],
    }
    if _int4_dtype is not None:
      out[i_].append(_int4_dtype)
      out[_int4_dtype] = []
    if _uint4_dtype is not None:
      out[i_].append(_uint4_dtype)
      out[_uint4_dtype] = []
    return out
  elif jax_numpy_dtype_promotion == 'strict':
    return {
      i_: [f_] + _int_types,
      f_: [c_] + _float_types,
      c_: _complex_types,
      **{t: [] for t in _jax_types}
    }
  else:
    raise ValueError(
      f"Unexpected value of jax_numpy_dtype_promotion={jax_numpy_dtype_promotion!r}")
