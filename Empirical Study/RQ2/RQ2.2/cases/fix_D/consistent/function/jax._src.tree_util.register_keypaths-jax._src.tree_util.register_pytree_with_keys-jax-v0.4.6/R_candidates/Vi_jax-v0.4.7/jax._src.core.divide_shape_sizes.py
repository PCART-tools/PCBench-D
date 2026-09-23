def divide_shape_sizes(s1: Shape, s2: Shape) -> DimSize:
  """Returns an integer "i" s.t., i * size(s2) == size(s1).
  Raises if there is no such integer."""
  s1 = s1 or (1,)
  s2 = s2 or (1,)
  handler, ds = _dim_handler_and_canonical(*s1, *s2)
  return handler.divide_shape_sizes(ds[:len(s1)], ds[len(s1):])
