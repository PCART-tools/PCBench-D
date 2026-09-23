def gt(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise greater-than: :math:`x > y`."""
  return gt_p.bind(x, y)
