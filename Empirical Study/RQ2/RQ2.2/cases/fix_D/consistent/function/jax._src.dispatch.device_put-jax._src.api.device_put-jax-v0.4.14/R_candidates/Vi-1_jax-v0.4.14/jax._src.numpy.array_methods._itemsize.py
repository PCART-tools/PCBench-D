def _itemsize(arr: ArrayLike) -> int:
  """Length of one array element in bytes."""
  return dtypes.dtype(arr, canonicalize=True).itemsize
