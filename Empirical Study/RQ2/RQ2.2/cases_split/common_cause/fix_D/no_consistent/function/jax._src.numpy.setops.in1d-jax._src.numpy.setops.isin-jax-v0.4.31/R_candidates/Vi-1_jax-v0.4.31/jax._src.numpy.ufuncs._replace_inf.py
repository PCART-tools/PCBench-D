def _replace_inf(x: ArrayLike) -> Array:
  return lax.select(isposinf(real(x)), lax._zeros(x), x)
