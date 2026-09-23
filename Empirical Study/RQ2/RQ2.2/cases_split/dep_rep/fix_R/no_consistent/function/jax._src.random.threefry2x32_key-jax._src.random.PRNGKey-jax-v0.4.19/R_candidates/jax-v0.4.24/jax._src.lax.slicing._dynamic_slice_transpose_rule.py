def _dynamic_slice_transpose_rule(t, operand, *start_indices, slice_sizes):
  assert ad.is_undefined_primal(operand)
  assert all(not ad.is_undefined_primal(s) for s in start_indices)
  operand_shape, operand_dtype = operand.aval.shape, operand.aval.dtype
  if type(t) is ad_util.Zero:
    return [ad_util.Zero(operand.aval)] + [None] * len(start_indices)
  else:
    zeros = lax.full(operand_shape, 0, operand_dtype)
    return ([dynamic_update_slice_p.bind(zeros, t, *start_indices)] +
            [None] * len(start_indices))
