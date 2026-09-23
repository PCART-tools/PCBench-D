def igamma(a: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise regularized incomplete gamma function."""
  return igamma_p.bind(a, x)
