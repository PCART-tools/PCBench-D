def symbolic_equal_shape(s1: Shape, s2: Shape) -> bool:
  return (len(s1) == len(s2) and
          all(unsafe_map(symbolic_equal_dim, s1, s2)))
