def reduce_window(operand, init_value, computation, window_dimensions,
                  window_strides, padding, base_dilation):
  op, dims, strides = operand, window_dimensions, window_strides
  if isinstance(padding, str):
    pads = padtype_to_pads(op.shape, dims, strides, padding)
  else:
    pads = padding
  op = op.reshape((1, 1) + op.shape)
  if base_dilation:
    op = _dilate(op, base_dilation, init_value)
  view = _conv_view(op, (1, 1) + dims, strides, pads,
                    pad_value=init_value)[0]
  view = view.reshape(view.shape[1:1+len(dims)] + (-1,))
  reducer = _make_reducer(computation, init_value)
  return reducer(view, axis=-1)
