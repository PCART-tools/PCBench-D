def _reduce_sum_padding_rule(in_avals, out_avals, operand, *, axes):
  del out_avals
  aval, = in_avals
  padded_axes = [(i, d.val) for i, d in enumerate(aval.shape)
                 if isinstance(d, pe.BoundedAxisSize)]
  masked_operand = _replace_masked_values(operand, 0, padded_axes)
  return [_reduce_sum(masked_operand, axes)]
