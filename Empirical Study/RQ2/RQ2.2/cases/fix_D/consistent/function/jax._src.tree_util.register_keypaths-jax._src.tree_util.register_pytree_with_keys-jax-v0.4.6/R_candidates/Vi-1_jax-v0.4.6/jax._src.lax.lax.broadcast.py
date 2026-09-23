def broadcast(operand: ArrayLike, sizes: Sequence[int]) -> Array:
  """Broadcasts an array, adding new leading dimensions

  Args:
    operand: an array
    sizes: a sequence of integers, giving the sizes of new leading dimensions
      to add to the front of the array.

  Returns:
    An array containing the result.

  See Also:
    jax.lax.broadcast_in_dim : add new dimensions at any location in the array shape.
  """
  dims = tuple(range(len(sizes), len(sizes) + np.ndim(operand)))
  return broadcast_in_dim(operand, tuple(sizes) + np.shape(operand), dims)
