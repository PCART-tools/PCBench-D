def _conv_general_dilated_masking_rule(
        padded_vals, logical_shapes, window_strides, padding, lhs_dilation,
        rhs_dilation, dimension_numbers, feature_group_count, batch_group_count,
        lhs_shape, rhs_shape, precision, preferred_element_type):
  lhs, rhs = padded_vals
  logical_lhs_shape, logical_rhs_shape = logical_shapes

  o, i, *window_dimensions = dimension_numbers.rhs_spec
  assert (np.all(np.take(rhs.shape, window_dimensions)
                  == np.take(logical_rhs_shape, window_dimensions))), \
              "Conv filter masking not yet implemented."

  n, c, *padded_dimensions = dimension_numbers.lhs_spec

  return conv_general_dilated(
    lax._masked(lhs, logical_lhs_shape, padded_dimensions),
    lax._masked(rhs, logical_rhs_shape, (i,)),
    window_strides=window_strides, padding=padding,
    lhs_dilation=lhs_dilation, rhs_dilation=rhs_dilation,
    dimension_numbers=dimension_numbers,
    feature_group_count=feature_group_count,
    batch_group_count=batch_group_count,
    precision=precision,
    preferred_element_type=preferred_element_type)
