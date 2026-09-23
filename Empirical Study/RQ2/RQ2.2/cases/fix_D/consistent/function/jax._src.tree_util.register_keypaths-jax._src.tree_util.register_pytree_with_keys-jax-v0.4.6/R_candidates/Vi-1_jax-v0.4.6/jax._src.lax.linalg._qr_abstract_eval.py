def _qr_abstract_eval(operand, *, full_matrices):
  if isinstance(operand, ShapedArray):
    if operand.ndim < 2:
      raise ValueError("Argument to QR decomposition must have ndims >= 2")
    *batch_dims, m, n = operand.shape
    k = m if full_matrices else min(m, n)
    q = operand.update(shape=(*batch_dims, m, k))
    r = operand.update(shape=(*batch_dims, k, n))
  else:
    q = operand
    r = operand
  return q, r
