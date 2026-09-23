def igamma(a: Array, x: Array) -> Array:
  r"""Elementwise regularized incomplete gamma function."""
  return igamma_p.bind(a, x)
