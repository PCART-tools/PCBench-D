def mul(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise multiplication: :math:`x \times y`."""
  return mul_p.bind(x, y)
