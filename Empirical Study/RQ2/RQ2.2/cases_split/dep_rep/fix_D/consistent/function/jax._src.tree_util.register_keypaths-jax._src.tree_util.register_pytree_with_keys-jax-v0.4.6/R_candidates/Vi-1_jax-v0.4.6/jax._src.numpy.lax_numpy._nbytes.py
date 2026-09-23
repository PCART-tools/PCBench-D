def _nbytes(arr: ArrayLike) -> int:
  """Total bytes consumed by the elements of the array."""
  return size(arr) * _dtype(arr).itemsize
