def _pow_jvp_lhs(g, ans, x, y):
  jac = mul(y, pow(x, select(eq(y, _zeros(y)), _ones(y), sub(y, _ones(y)))))
  return mul(g, jac)
