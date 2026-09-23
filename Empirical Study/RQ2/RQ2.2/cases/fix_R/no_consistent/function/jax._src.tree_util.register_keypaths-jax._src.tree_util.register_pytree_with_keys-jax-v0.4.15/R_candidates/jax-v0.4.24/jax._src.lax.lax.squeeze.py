def squeeze(array: ArrayLike, dimensions: Sequence[int]) -> Array:
  """Squeeze any number of size 1 dimensions from an array."""
  ndim = np.ndim(array)
  dimensions = tuple(sorted(canonicalize_axis(i, ndim) for i in dimensions))
  if not dimensions and isinstance(array, Array):
    return type_cast(Array, array)
  return squeeze_p.bind(array, dimensions=dimensions)
