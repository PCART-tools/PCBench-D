def betainc(a: ArrayLike, b: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise regularized incomplete beta integral."""
  return regularized_incomplete_beta_p.bind(a, b, x)
