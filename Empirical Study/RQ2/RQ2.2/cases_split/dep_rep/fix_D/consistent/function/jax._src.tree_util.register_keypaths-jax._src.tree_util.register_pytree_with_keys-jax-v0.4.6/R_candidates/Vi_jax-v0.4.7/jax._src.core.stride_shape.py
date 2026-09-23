def stride_shape(s: Shape, window_size: Shape, window_stride: Shape) -> Shape:
  """(s - window_size) // window_stride + 1"""
  return tuple(map(stride_dim, s, window_size, window_stride))
