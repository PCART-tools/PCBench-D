def _slice_transpose_rule(t, operand, *, start_indices, limit_indices, strides):
  assert ad.is_undefined_primal(operand)
  operand_shape = operand.aval.shape
  if strides is None or np.all(np.equal(strides, 1)):
    pads = zip(start_indices, np.subtract(operand_shape, limit_indices),
               (0,) * len(start_indices))
  else:
    real_limits = np.add(
      start_indices,
      np.where(np.array(t.shape) == 0, 0,
               np.add(1, np.multiply(np.subtract(t.shape, 1), strides))))
    pads = zip(start_indices, np.subtract(operand_shape, real_limits),
               np.subtract(strides, 1))
  result = lax.pad(t, lax._const(t, 0), pads)
  assert result.shape == operand_shape, f"{result.shape=} {operand_shape=}"
  return [result]
