def _qr_translation_rule(ctx, avals_in, avals_out, operand, *, full_matrices):
  operand_aval, = avals_in
  shape = operand_aval.shape
  m, n = shape[-2:]
  if m == 0 or n == 0:
    return [_eye_like_xla(ctx.builder, avals_out[0]),
            _zeros_like_xla(ctx.builder, avals_out[1])]
  return xops.QR(operand, full_matrices)
