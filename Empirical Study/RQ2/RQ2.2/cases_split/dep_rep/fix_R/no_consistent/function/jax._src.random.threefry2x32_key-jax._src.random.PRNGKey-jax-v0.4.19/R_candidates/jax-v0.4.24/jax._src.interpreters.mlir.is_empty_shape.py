def is_empty_shape(s: core.Shape) -> bool:
  return any(d == 0 for d in s)
