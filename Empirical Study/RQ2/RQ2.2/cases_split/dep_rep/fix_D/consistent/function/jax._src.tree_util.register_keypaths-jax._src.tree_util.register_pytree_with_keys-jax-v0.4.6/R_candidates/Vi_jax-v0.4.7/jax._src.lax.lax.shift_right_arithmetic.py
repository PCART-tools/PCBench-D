def shift_right_arithmetic(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise arithmetic right shift: :math:`x \gg y`."""
  return shift_right_arithmetic_p.bind(x, y)
