def _tri(dtype: DTypeLike, shape: Shape, offset: int) -> Array:
  """Like numpy.tri, create a 2D array with ones below a diagonal."""
  offset = int(offset)
  dtype = dtypes.canonicalize_dtype(dtype)
  bool_tri = ge(add(broadcasted_iota(np.int32, shape, 0), np.int32(offset)),
                broadcasted_iota(np.int32, shape, 1))
  return convert_element_type_p.bind(bool_tri, new_dtype=dtype, weak_type=False)
