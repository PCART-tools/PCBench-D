def _replace_inf(x):
  return lax.select(isposinf(real(x)), lax_internal._zeros(x), x)
