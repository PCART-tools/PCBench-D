def lt(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise less-than: :math:`x < y`."""
  return lt_p.bind(x, y)
