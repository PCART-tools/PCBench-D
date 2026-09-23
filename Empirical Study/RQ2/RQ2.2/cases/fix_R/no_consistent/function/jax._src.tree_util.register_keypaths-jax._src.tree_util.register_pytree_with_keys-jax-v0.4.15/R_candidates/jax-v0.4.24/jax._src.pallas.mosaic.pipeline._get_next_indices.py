def _get_next_indices(grid: core.StaticGrid, indices: GridIndices) -> GridIndices:
  """Takes a grid and current indices and returns the next indices.

  grid: (3, 4, 5)
  indices: [1, 0, 4]
  returns: [1, 1, 0]

  Args:
    grid: Grid spec.
    indices: Current indices.

  Returns:
    Incremented indices.
  """
  next_indices = []
  carry = True
  for dim_size, index in reversed(list(zip(grid, indices))):
    i = jnp.where(carry, index + 1, index)
    carry = dim_size == i
    next_indices.append(jnp.where(carry, 0, i))
  return tuple(reversed(next_indices))
