def integer_pow(x: ArrayLike, y: int) -> Array:
  r"""Elementwise power: :math:`x^y`, where :math:`y` is a fixed integer."""
  return integer_pow_p.bind(x, y=y)
