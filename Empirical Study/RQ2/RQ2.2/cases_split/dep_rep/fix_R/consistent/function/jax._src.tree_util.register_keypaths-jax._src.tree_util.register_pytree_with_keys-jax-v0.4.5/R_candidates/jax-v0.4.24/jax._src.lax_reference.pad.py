def pad(operand, padding_value, padding_config):
  # https://www.tensorflow.org/xla/operation_semantics#pad
  lo, hi, interior = util.unzip3(padding_config)
  # Handle first the positive edge padding and interior
  lo_pos, hi_pos = np.clip(lo, 0, None), np.clip(hi, 0, None)
  outshape = np.add(np.add(np.add(lo_pos, hi_pos), operand.shape),
                     np.multiply(interior, np.subtract(operand.shape, 1)))
  out = np.full(outshape, padding_value, operand.dtype)
  lhs_slices = tuple(_slice(l if l > 0 else 0, -h if h > 0 else None, step)
                     for l, h, step in zip(lo_pos, hi_pos, np.add(1, interior)))
  out[lhs_slices] = operand
  trim_slices = tuple(_slice(-l if l < 0 else 0, h if h < 0 else None)
                     for l, h in zip(lo, hi))
  return out[trim_slices]
