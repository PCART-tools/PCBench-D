def _squeeze_lower(ctx, operand, *, dimensions):
  del dimensions  # Implied by the output aval.
  return [mlir.reshape(ctx, operand, ctx.avals_out[0])]
