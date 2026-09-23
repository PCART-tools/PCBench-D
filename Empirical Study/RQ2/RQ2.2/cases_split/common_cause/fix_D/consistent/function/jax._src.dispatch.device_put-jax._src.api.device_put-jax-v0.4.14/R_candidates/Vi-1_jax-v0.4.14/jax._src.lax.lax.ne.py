def ne(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise not-equals: :math:`x \neq y`."""
  return ne_p.bind(x, y)
