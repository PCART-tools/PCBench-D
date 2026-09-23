def _qr_impl(operand, *, full_matrices):
  q, r = dispatch.apply_primitive(qr_p, operand, full_matrices=full_matrices)
  return q, r
