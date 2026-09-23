def sub(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise subtraction: :math:`x - y`."""
  return sub_p.bind(x, y)
