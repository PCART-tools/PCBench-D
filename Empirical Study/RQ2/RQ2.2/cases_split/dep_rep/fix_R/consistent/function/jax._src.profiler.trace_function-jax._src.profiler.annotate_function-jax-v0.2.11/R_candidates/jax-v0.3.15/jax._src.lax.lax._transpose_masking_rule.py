def _transpose_masking_rule(padded_vals, logical_shapes, permutation):
  return transpose(*padded_vals, permutation=permutation)
