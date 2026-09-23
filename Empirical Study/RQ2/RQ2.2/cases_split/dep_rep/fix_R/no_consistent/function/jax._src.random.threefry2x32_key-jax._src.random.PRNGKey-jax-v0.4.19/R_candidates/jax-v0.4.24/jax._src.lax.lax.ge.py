def ge(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise greater-than-or-equals: :math:`x \geq y`."""
  return ge_p.bind(x, y)
