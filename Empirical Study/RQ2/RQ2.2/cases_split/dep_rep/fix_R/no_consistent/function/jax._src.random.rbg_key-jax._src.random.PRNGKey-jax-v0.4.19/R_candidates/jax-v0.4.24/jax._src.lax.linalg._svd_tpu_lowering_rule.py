def _svd_tpu_lowering_rule(ctx, operand, *, full_matrices, compute_uv):
  operand_aval, = ctx.avals_in
  m, n = operand_aval.shape[-2:]

  if m == 0 or n == 0:
    return mlir.lower_fun(_empty_svd, multiple_results=True)(
      ctx, operand, full_matrices=full_matrices, compute_uv=compute_uv)

  return mlir.lower_fun(_svd_tpu, multiple_results=True)(
      ctx, operand, full_matrices=full_matrices, compute_uv=compute_uv)
