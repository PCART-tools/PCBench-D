def expm1(x: Array) -> Array:
  r"""Elementwise :math:`e^{x} - 1`."""
  return expm1_p.bind(x)
