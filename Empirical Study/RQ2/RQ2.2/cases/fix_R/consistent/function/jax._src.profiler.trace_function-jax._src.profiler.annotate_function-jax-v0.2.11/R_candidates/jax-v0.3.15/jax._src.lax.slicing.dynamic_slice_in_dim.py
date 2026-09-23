def dynamic_slice_in_dim(operand: Array, start_index: Array,
                         slice_size: int, axis: int = 0) -> Array:
  """Convenience wrapper around dynamic_slice applying to one dimension."""
  start_indices = [lax._zero(start_index)] * operand.ndim
  slice_sizes = list(operand.shape)

  axis = int(axis)
  start_indices[axis] = start_index
  slice_sizes[axis] = core._canonicalize_dimension(slice_size)
  return dynamic_slice(operand, start_indices, slice_sizes)
