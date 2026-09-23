def _create_token_lowering(ctx, *operands):
  aval_out, = ctx.avals_out
  return mhlo.CreateTokenOp(mlir.aval_to_ir_type(aval_out)).results
