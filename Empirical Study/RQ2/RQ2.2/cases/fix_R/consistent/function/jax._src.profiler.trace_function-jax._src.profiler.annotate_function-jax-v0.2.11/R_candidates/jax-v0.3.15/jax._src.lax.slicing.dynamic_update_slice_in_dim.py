def dynamic_update_slice_in_dim(operand: Array, update: Array,
                                start_index: Array, axis: int) -> Array:
  """Convenience wrapper around :func:`dynamic_update_slice` to update a slice
     in a single ``axis``.
  """
  axis = int(axis)
  start_indices = [lax._zero(start_index)] * lax._ndim(operand)
  start_indices[axis] = start_index
  return dynamic_update_slice(operand, update, start_indices)
