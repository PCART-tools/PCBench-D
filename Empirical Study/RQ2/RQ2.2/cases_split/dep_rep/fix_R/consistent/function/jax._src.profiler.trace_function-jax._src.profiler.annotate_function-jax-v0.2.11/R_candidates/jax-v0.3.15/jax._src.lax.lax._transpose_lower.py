def _transpose_lower(ctx, x, *, permutation):
  aval_out, = ctx.avals_out
  return mhlo.TransposeOp(x, mlir.dense_int_elements(permutation)).results
