def conv_with_general_padding(
    lhs, rhs, window_strides, padding, lhs_dilation, rhs_dilation):
  return _conv(_dilate(lhs, lhs_dilation), _dilate(rhs, rhs_dilation),
               window_strides, padding)
