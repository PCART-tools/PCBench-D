def _integer_pow(a, *, y):
  if y == 2:
    return a * a
  if y == 3:
    return a * a * a
  if y == -2:
    return 1.0 / (a * a)
  return jax.lax.pow(a, y)
