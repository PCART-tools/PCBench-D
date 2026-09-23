def slice_in_dim(operand: Union[Array, np.ndarray], start_index: Optional[int],
                 limit_index: Optional[int],
                 stride: int = 1, axis: int = 0) -> Array:
  """Convenience wrapper around slice applying to only one dimension."""
  start_indices = [0] * operand.ndim
  limit_indices = list(operand.shape)
  strides = [1] * operand.ndim

  # translate `None`
  len_axis = operand.shape[axis]
  start_index_int = (core._canonicalize_dimension(start_index)
                     if start_index is not None else 0)
  limit_index_int = (core._canonicalize_dimension(limit_index)
                     if limit_index is not None else len_axis)

  # translate negative indices
  if start_index_int < 0:
    start_index_int = start_index_int + len_axis
  if limit_index_int < 0:
    limit_index_int = limit_index_int + len_axis

  axis = int(axis)
  start_indices[axis] = start_index_int
  limit_indices[axis] = limit_index_int
  strides[axis] = int(stride)

  return slice(operand, start_indices, limit_indices, strides)
