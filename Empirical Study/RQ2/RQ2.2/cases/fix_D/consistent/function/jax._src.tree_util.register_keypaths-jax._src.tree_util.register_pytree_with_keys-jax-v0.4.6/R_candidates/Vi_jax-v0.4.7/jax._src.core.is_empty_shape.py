def is_empty_shape(s: Shape) -> bool:
  return any(symbolic_equal_dim(d, 0) for d in s)
