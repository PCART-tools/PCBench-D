def reduce_window_shape_tuple(operand_shape, window_dimensions, window_strides,
                              padding, base_dilation=None,
                              window_dilation=None):
  if base_dilation is not None:
    operand_shape = lax._dilate_shape(operand_shape, base_dilation)
  if window_dilation is not None:
    window_dimensions = lax._dilate_shape(window_dimensions, window_dilation)
  pads_lo, pads_hi = util.unzip2(padding)
  operand_padded = core.sum_shapes(operand_shape, pads_lo, pads_hi)
  return core.stride_shape(operand_padded, window_dimensions, window_strides)
