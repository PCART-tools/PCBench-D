def _isnan(x: ArrayLike) -> Array:
  return lax.ne(x, x)
