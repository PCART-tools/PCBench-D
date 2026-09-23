def shift_left(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise left shift: :math:`x \ll y`."""
  return shift_left_p.bind(x, y)
