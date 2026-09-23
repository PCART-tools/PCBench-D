def _tridiagonal_cpu_gpu_hlo(sytrd_impl, ctx, a, *, lower):
  a_aval, = ctx.avals_in
  a, d, e, taus, info = sytrd_impl(a_aval.dtype, a, lower=lower)
  return a, d, e, taus, info
