def dilate_shape(s: Shape, dilations: Sequence[int]) -> Shape:
  return tuple(map(dilate_dim, s, dilations))
