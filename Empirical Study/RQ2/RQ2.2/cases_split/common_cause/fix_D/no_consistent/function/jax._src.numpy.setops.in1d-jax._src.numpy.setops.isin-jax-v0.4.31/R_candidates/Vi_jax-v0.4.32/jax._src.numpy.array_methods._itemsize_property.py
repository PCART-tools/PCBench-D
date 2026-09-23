def _itemsize_property(self: Array) -> int:
  """Length of one array element in bytes."""
  return dtypes.dtype(self, canonicalize=True).itemsize
