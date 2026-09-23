def _promote_integer_dtype(dtype: DTypeLike) -> DTypeLike:
  # Note: NumPy always promotes to 64-bit; jax instead promotes to the
  # default dtype as defined by dtypes.int_ or dtypes.uint.
  if dtypes.issubdtype(dtype, np.bool_):
    return dtypes.int_
  elif dtypes.issubdtype(dtype, np.unsignedinteger):
    if np.iinfo(dtype).bits < np.iinfo(dtypes.uint).bits:
      return dtypes.uint
  elif dtypes.issubdtype(dtype, np.integer):
    if np.iinfo(dtype).bits < np.iinfo(dtypes.int_).bits:
      return dtypes.int_
  return dtype
