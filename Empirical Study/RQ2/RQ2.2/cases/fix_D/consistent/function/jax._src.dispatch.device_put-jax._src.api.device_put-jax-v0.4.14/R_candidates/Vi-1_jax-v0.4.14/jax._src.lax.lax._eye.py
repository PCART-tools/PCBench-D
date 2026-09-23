def _eye(dtype: DTypeLike, shape: Shape, offset: int) -> Array:
  """Like numpy.eye, create a 2D array with ones on a diagonal."""
  offset = int(offset)
  dtype = dtypes.canonicalize_dtype(dtype)
  bool_eye = eq(add(broadcasted_iota(np.int32, shape, 0), np.int32(offset)),
                broadcasted_iota(np.int32, shape, 1))
  return convert_element_type_p.bind(bool_eye, new_dtype=dtype, weak_type=False)
