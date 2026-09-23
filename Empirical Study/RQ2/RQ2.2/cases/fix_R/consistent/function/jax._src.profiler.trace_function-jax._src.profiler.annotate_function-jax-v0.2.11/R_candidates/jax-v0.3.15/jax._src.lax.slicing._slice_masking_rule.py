def _slice_masking_rule(
    padded_vals, logical_shapes, start_indices, limit_indices, strides):
  operand, = padded_vals
  strides = masking.padded_shape_as_value(strides) if strides else None
  return slice(operand,
               start_indices=masking.padded_shape_as_value(start_indices),
               limit_indices=masking.padded_shape_as_value(limit_indices),
               strides=strides)
