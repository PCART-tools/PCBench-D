def _nbytes(arr: ArrayLike) -> int:
  """Total bytes consumed by the elements of the array."""
  return np.size(arr) * dtypes.dtype(arr, canonicalize=True).itemsize
