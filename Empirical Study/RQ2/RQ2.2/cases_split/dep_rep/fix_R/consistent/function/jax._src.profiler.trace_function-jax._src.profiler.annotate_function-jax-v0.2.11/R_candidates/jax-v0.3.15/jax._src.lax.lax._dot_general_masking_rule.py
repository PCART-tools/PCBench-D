def _dot_general_masking_rule(padded_vals, logical_shapes, *, dimension_numbers,
                              precision,
                              preferred_element_type: Optional[DType]):
  lhs, rhs = padded_vals
  # Only need to mask off contraction dims of one side - we mask the lhs here
  # but this is arbitrary. Could check the sizes of lhs and rhs and mask
  # whichever is smallest.
  lhs_shape, _ = logical_shapes
  (lhs_contract, _), _ = dimension_numbers
  return dot_general(_masked(lhs, lhs_shape, lhs_contract),
                     rhs, dimension_numbers, precision=precision,
                     preferred_element_type=preferred_element_type)
