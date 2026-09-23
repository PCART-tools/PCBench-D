def _dot_general_padding_rule(in_avals, out_avals, lhs, rhs, *,
                              dimension_numbers, **params):
  lhs_aval, _ = in_avals
  (lhs_contract, _), _ = dimension_numbers
  padded_axes = [(i, lhs_aval.shape[i].val) for i in lhs_contract
                 if isinstance(lhs_aval.shape[i], pe.BoundedAxisSize)]
  lhs_ = _replace_masked_values(lhs, 0, padded_axes)
  return [dot_general(lhs_, rhs, dimension_numbers=dimension_numbers, **params)]
