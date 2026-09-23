def igammac(a: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise complementary regularized incomplete gamma function."""
  return igammac_p.bind(a, x)
