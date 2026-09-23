def add(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise addition: :math:`x + y`."""
  return add_p.bind(x, y)
