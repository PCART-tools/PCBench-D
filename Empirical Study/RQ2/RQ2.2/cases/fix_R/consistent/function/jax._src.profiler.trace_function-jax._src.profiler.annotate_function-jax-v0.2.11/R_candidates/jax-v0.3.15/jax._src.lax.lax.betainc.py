def betainc(a: Array, b: Array, x: Array) -> Array:
  r"""Elementwise regularized incomplete beta integral."""
  return regularized_incomplete_beta_p.bind(a, b, x)
