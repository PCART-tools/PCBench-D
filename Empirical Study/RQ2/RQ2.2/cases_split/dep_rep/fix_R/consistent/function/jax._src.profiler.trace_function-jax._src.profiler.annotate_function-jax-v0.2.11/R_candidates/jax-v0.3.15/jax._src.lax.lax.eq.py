def eq(x: Array, y: Array) -> Array:
  r"""Elementwise equals: :math:`x = y`."""
  return eq_p.bind(x, y)
