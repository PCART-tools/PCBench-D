def dslice(start: int |  Array | None, size: int | None = None
           ) -> slice | Slice:
  """Constructs a `Slice` from a start and a size."""
  if start is None:
    return slice(None)
  if size is None:
    if not isinstance(start, int):
      raise ValueError("Non-static `dslice`")
    return Slice(0, start)
  return Slice(start, size)
