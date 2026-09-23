def sum_shapes(*ss: Shape) -> Shape:
  return tuple(map(sum_dim, *ss))
