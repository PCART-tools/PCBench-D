def conv_general_dilated(lhs, rhs, window_strides, padding, lhs_dilation,
                         rhs_dilation, dimension_numbers):
  lhs_perm, rhs_perm, out_perm = _conv_general_permutations(dimension_numbers)
  if isinstance(padding, str):
    padding = padtype_to_pads(np.take(lhs.shape, lhs_perm)[2:],
                              np.take(rhs.shape, rhs_perm)[2:],
                              window_strides, padding)
  trans_lhs = transpose(lhs, lhs_perm)
  trans_rhs = transpose(rhs, rhs_perm)
  out = conv_with_general_padding(trans_lhs, trans_rhs, window_strides, padding,
                                  lhs_dilation, rhs_dilation)
  return transpose(out, np.argsort(out_perm))
