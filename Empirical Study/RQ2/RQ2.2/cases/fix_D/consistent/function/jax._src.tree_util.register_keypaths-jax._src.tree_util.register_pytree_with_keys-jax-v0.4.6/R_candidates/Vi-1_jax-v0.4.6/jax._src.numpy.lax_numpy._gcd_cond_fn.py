def _gcd_cond_fn(xs: Tuple[Array, Array]) -> Array:
  x1, x2 = xs
  return reductions.any(x2 != 0)
