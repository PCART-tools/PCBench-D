def eq(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise equals: :math:`x = y`."""
  return eq_p.bind(x, y)
