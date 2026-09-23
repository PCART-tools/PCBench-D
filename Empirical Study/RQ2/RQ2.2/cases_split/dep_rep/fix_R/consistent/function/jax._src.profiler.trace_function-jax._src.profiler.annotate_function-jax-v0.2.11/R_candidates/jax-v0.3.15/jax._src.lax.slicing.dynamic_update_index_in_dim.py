def dynamic_update_index_in_dim(operand: Array, update: Array, index: Array,
                                axis: int) -> Array:
  """Convenience wrapper around :func:`dynamic_update_slice` to update a slice
     of size 1 in a single ``axis``.
  """
  axis = int(axis)
  if lax._ndim(update) != lax._ndim(operand):
    assert lax._ndim(update) + 1 == lax._ndim(operand)
    update = lax.expand_dims(update, (axis,))
  return dynamic_update_slice_in_dim(operand, update, index, axis)
