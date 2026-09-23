def expand_dims(array: Array, dimensions: Sequence[int]) -> Array:
  """Insert any number of size 1 dimensions into an array."""
  if len(set(dimensions)) != len(dimensions):
    raise ValueError(f'repeated axis in lax.expand_dims: {dimensions}')
  ndim_out = np.ndim(array) + len(dimensions)
  dims = [canonicalize_axis(i, ndim_out) for i in dimensions]
  if len(set(dims)) != len(dims):  # check again after canonicalizing
    raise ValueError(f'repeated axis in lax.expand_dims: {dims}')
  dims_set = frozenset(dims)
  result_shape = list(np.shape(array))
  for i in sorted(dims_set):
    result_shape.insert(i, 1)
  broadcast_dims = [i for i in range(ndim_out) if i not in dims_set]
  return broadcast_in_dim(array, result_shape, broadcast_dims)
