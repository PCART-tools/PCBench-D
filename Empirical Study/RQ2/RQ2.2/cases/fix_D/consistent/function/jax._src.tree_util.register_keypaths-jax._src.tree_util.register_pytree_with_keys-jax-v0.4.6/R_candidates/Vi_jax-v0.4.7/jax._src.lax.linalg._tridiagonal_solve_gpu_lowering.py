def _tridiagonal_solve_gpu_lowering(lowering, ctx, dl, d, du, b, *, m, n, ldb, t):
  return [lowering(dl, d, du, b, m=m, n=n, ldb=ldb,
                   t=dtypes.canonicalize_dtype(t))]
