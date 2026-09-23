def index_in_dim(operand: Array, index: int, axis: int = 0,
                 keepdims: bool = True) -> Array:
  """Convenience wrapper around slice to perform int indexing."""
  index, axis = core._canonicalize_dimension(index), int(axis)
  axis_size = operand.shape[axis]
  wrapped_index = index + axis_size if index < 0 else index
  if not 0 <= wrapped_index < axis_size:
    msg = 'index {} is out of bounds for axis {} with size {}'
    raise IndexError(msg.format(index, axis, axis_size))
  result = slice_in_dim(operand, wrapped_index, wrapped_index + 1, 1, axis)
  if keepdims:
    return result
  else:
    return lax.squeeze(result, (axis,))
