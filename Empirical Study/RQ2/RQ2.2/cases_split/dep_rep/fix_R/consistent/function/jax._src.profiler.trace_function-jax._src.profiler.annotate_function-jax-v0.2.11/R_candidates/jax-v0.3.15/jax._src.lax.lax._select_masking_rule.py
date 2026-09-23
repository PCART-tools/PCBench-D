def _select_masking_rule(padded_vals, logical_shapes):
  which_shape, true_shape, false_shape = (
      masking.padded_shape_as_value(val.shape) for val in padded_vals)
  assert np.array_equal(which_shape, true_shape)
  assert np.array_equal(which_shape, false_shape)
  return select_n(*padded_vals)
