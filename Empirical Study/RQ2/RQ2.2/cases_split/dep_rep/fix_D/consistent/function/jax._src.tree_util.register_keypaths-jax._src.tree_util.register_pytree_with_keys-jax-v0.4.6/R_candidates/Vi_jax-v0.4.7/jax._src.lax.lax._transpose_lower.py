def _transpose_lower(ctx, x, *, permutation):
  aval_out, = ctx.avals_out
  if core.is_opaque_dtype(aval_out.dtype):
    return [aval_out.dtype._rules.transpose_mlir(ctx, aval_out, x, permutation=permutation)]
  return hlo.TransposeOp(x, mlir.dense_int_elements(permutation)).results
