def lt(x: Array, y: Array) -> Array:
  r"""Elementwise less-than: :math:`x < y`."""
  return lt_p.bind(x, y)
