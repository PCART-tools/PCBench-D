def mul(x: Array, y: Array) -> Array:
  r"""Elementwise multiplication: :math:`x \times y`."""
  return mul_p.bind(x, y)
