def _integer_pow_jvp(g, x, *, y):
  return _zeros(g) if y == 0 else mul(g, mul(_const(x, y), integer_pow(x, y - 1)))
