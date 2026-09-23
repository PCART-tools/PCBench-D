def _gcd_cond_fn(xs):
  x1, x2 = xs
  return any(x2 != 0)
