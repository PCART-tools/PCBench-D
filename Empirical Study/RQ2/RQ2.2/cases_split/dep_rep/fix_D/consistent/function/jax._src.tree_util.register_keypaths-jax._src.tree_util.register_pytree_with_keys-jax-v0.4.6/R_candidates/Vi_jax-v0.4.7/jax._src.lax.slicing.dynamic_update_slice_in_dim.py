def dynamic_update_slice_in_dim(operand: Union[Array, np.ndarray],
                                update: ArrayLike,
                                start_index: ArrayLike, axis: int) -> Array:
  """Convenience wrapper around :func:`dynamic_update_slice` to update a slice
     in a single ``axis``.
  """
  axis = int(axis)
  start_indices: List[ArrayLike] = [lax._const(start_index, 0)] * lax._ndim(operand)
  start_indices[axis] = start_index
  return dynamic_update_slice(operand, update, start_indices)
