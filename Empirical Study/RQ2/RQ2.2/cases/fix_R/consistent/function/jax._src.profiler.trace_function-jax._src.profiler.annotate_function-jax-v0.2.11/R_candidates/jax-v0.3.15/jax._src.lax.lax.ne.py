def ne(x: Array, y: Array) -> Array:
  r"""Elementwise not-equals: :math:`x \neq y`."""
  return ne_p.bind(x, y)
