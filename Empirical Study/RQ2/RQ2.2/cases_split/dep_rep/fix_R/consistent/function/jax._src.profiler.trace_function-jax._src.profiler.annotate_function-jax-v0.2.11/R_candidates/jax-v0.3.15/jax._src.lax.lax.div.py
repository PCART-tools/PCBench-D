def div(x: Array, y: Array) -> Array:
  r"""Elementwise division: :math:`x \over y`."""
  return div_p.bind(x, y)
