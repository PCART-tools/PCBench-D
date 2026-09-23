def _lu_tpu_translation_rule(ctx, avals_in, avals_out, operand):
  return xops.LU(operand)
