def is_empty_shape(s: Shape) -> bool:
  return any(definitely_equal(d, 0) for d in s)
