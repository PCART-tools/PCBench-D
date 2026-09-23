def _tridiagonal_solve_gpu_lowering(lowering, ctx, dl, d, du, b, *, m, n, ldb, t):
  _, _, _, b_aval = ctx.avals_in
  b_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, b_aval.shape)
  return [lowering(
      dl, d, du, b, m=m, n=n, ldb=ldb, t=dtypes.canonicalize_dtype(t),
      b_shape_vals=b_shape_vals)]
