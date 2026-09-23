def _normalize_index(index, axis_size):
  """Normalizes an index value in the range [-N, N) to the range [0, N)."""
  if issubdtype(_dtype(index), np.unsignedinteger):
    return index
  if core.is_constant_dim(axis_size):
    axis_size_val = _lax_const(index, axis_size)
  else:
    axis_size_val = lax.convert_element_type(core.dimension_as_value(axis_size),
                                             _dtype(index))
  return lax.select(
    lax.lt(index, _lax_const(index, 0)),
    lax.add(index, axis_size_val),
    index)
