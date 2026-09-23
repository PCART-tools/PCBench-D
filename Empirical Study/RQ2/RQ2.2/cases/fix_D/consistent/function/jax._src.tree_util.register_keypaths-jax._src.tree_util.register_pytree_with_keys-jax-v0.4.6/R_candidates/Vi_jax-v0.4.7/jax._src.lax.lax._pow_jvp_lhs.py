def _pow_jvp_lhs(g, ans, x, y):
  return mul(g, mul(y, pow(x, sub(y, _ones(y)))))
