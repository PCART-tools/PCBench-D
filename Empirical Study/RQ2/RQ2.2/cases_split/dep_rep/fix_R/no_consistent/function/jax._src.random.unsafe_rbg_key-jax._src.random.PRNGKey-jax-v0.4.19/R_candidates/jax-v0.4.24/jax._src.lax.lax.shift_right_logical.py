def shift_right_logical(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise logical right shift: :math:`x \gg y`."""
  return shift_right_logical_p.bind(x, y)
