def _tridiagonal_solve_transpose_rule(cotangent, dl, d, du, b, *, m, n, ldb, t):
  del m, n, ldb, t
  # Tridiagonal solve is nonlinear in the tridiagonal arguments and linear
  # otherwise.
  assert not (ad.is_undefined_primal(dl) or ad.is_undefined_primal(d) or
              ad.is_undefined_primal(du)) and ad.is_undefined_primal(b)
  if type(cotangent) is ad_util.Zero:
    cotangent_b = ad_util.Zero(b.aval)
  else:
    cotangent_b = tridiagonal_solve(dl, d, du, cotangent)
  return [None, None, None, cotangent_b]
