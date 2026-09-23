def _itemsize(arr: ArrayLike) -> int:
  """Length of one array element in bytes."""
  return _dtype(arr).itemsize
