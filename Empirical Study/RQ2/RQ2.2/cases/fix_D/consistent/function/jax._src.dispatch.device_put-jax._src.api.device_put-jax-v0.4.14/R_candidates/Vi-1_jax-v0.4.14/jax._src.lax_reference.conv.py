def conv(lhs, rhs, window_strides, padding):
  pads = padtype_to_pads(lhs.shape[2:], rhs.shape[2:], window_strides, padding)
  return _conv(lhs, rhs, window_strides, pads)
