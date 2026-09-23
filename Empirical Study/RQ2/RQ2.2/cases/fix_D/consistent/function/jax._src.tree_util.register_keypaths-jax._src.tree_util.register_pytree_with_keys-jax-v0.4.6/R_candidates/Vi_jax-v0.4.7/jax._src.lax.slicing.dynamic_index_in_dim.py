def dynamic_index_in_dim(operand: Union[Array, np.ndarray],
                         index: Union[int, Array],
                         axis: int = 0, keepdims: bool = True) -> Array:
  """Convenience wrapper around dynamic_slice to perform int indexing."""
  result = dynamic_slice_in_dim(operand, index, 1, axis)
  if keepdims:
    return result
  else:
    return lax.squeeze(result, (axis,))
