def greater_equal_shape(s1: Shape, s2: Shape) -> bool:
  return all(map(greater_equal_dim, s1, s2))
