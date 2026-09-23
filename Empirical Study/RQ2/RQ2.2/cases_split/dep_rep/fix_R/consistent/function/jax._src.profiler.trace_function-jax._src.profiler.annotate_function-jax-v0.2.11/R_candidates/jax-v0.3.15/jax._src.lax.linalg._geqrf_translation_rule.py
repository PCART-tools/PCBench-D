def _geqrf_translation_rule(ctx, avals_in, avals_out, operand):
  return xops.QrDecomposition(operand)
