def pow(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise power: :math:`x^y`."""
  return pow_p.bind(x, y)
