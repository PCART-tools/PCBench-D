def _pow_jvp_rhs(g, ans, x, y):
  return mul(g, mul(log(_replace_zero(x)), ans))
