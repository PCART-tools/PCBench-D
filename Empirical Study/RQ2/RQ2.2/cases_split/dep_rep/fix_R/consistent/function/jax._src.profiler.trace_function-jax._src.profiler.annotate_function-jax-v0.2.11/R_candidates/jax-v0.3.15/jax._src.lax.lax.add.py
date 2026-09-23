def add(x: Array, y: Array) -> Array:
  r"""Elementwise addition: :math:`x + y`."""
  return add_p.bind(x, y)
