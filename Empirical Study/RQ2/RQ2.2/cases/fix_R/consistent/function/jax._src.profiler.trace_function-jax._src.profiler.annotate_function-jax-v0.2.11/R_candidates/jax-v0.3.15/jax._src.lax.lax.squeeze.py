def squeeze(array: Array, dimensions: Sequence[int]) -> Array:
  """Squeeze any number of size 1 dimensions from an array."""
  ndim = np.ndim(array)
  dimensions = tuple(sorted(canonicalize_axis(i, ndim) for i in dimensions))
  if not dimensions:
    return array
  return squeeze_p.bind(array, dimensions=dimensions)
