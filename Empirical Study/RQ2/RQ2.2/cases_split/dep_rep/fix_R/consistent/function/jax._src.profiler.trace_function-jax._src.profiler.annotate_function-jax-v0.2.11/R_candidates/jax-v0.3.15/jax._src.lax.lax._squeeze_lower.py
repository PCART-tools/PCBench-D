def _squeeze_lower(ctx, operand, *, dimensions):
  del dimensions  # Implied by the output aval.
  aval_out, = ctx.avals_out
  return mhlo.ReshapeOp(mlir.aval_to_ir_type(aval_out), operand).results
