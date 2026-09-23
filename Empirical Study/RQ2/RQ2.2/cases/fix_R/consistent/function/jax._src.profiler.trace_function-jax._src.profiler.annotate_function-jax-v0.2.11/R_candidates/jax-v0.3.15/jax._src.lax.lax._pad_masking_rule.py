def _pad_masking_rule(padded_vals, logical_shapes, padding_config):
  operand, padding_value = padded_vals
  shape, _ = logical_shapes

  out = pad(operand, padding_value, padding_config)
  out_shape = [lo + shape[i] * (interior + 1)
               for i, (lo, hi, interior) in enumerate(padding_config)]
  padded_dims = [i for i, config in enumerate(padding_config)
                 if config != (0, 0, 0)]
  return _masked(out, out_shape, padded_dims, padding_value)
