def gt(x: Array, y: Array) -> Array:
  r"""Elementwise greater-than: :math:`x > y`."""
  return gt_p.bind(x, y)
