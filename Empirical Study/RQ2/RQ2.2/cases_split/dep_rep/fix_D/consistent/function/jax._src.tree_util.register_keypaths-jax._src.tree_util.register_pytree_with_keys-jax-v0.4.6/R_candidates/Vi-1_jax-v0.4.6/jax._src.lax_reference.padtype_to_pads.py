def padtype_to_pads(in_shape, filter_shape, window_strides, padding):
  if padding.upper() == 'SAME':
    out_shape = np.ceil(np.true_divide(in_shape, window_strides)).astype(int)
    pad_sizes = [_max((out_size - 1) * stride + filter_size - in_size, 0)
                 for out_size, stride, filter_size, in_size
                 in zip(out_shape, window_strides, filter_shape, in_shape)]
    return [(pad_size // 2, pad_size - pad_size // 2) for pad_size in pad_sizes]
  else:
    return [(0, 0)] * len(in_shape)
