def igammac(a: Array, x: Array) -> Array:
  r"""Elementwise complementary regularized incomplete gamma function."""
  return igammac_p.bind(a, x)
