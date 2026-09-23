def pow(x: Array, y: Array) -> Array:
  r"""Elementwise power: :math:`x^y`."""
  return pow_p.bind(x, y)
