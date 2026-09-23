def _after_all_lowering(ctx, *operands):
  aval_out, = ctx.avals_out
  return mhlo.AfterAllOp(mlir.aval_to_ir_type(aval_out), operands).results
