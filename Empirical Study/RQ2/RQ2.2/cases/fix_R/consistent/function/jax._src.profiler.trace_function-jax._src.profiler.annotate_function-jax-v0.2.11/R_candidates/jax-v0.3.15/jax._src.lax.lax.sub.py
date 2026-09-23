def sub(x: Array, y: Array) -> Array:
  r"""Elementwise subtraction: :math:`x - y`."""
  return sub_p.bind(x, y)
