def _dynamic_update_slice_transpose_rule(t, operand, update, *start_indices):
  assert all(not ad.is_undefined_primal(x) for x in start_indices)
  if ad.is_undefined_primal(update):
    update_shape = update.aval.shape
  else:
    update_shape = update.shape
  if type(t) is ad_util.Zero:
    operand_t = ad_util.Zero(operand.aval) if ad.is_undefined_primal(operand) else None
    update_t = ad_util.Zero(update.aval) if ad.is_undefined_primal(update) else None
  else:
    dus = dynamic_update_slice
    ds = dynamic_slice
    zeros = lax._zeros(t, shape=update_shape)
    operand_t = dus(t, zeros, start_indices) if ad.is_undefined_primal(operand) else None
    update_t = ds(t, start_indices, update_shape) if ad.is_undefined_primal(update) else None
  return [operand_t, update_t] + [None] * len(start_indices)
