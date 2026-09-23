def padtype_to_pads(in_shape, window_shape, window_strides, padding):
  """Convert padding string to list of pairs of pad values."""

  if isinstance(padding, str):
    mapping = {
        'VALID': PaddingType.VALID,
        'SAME': PaddingType.SAME,
        'SAME_LOWER': PaddingType.SAME_LOWER,
    }
    try:
      padding = mapping[padding.upper()]
    except KeyError as err:
      msg = "Unrecognized padding type: expected 'VALID' or 'SAME', got {}."
      raise RuntimeError(msg.format(padding)) from err

  if padding == PaddingType.SAME or padding == PaddingType.SAME_LOWER:
    out_shape = _ceil_divide(in_shape, window_strides)
    pad_sizes = np.maximum(0, (out_shape - 1) * window_strides +
                                window_shape - in_shape)
    if padding == PaddingType.SAME:
      return [
          (pad_size // 2, pad_size - pad_size // 2) for pad_size in pad_sizes
      ]
    else:
      return [
          (pad_size - pad_size // 2, pad_size // 2) for pad_size in pad_sizes
      ]
  elif padding == PaddingType.VALID:
    return [(0, 0)] * len(in_shape)
  else:
    msg = "Unknown padding type: {}."
    raise TypeError(msg.format(padding))
