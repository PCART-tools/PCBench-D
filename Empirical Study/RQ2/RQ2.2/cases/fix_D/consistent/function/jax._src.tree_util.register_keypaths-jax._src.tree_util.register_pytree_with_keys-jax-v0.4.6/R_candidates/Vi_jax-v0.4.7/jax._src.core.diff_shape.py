def diff_shape(s1: Shape, s2: Shape) -> Shape:
  return tuple(map(diff_dim, s1, s2))
