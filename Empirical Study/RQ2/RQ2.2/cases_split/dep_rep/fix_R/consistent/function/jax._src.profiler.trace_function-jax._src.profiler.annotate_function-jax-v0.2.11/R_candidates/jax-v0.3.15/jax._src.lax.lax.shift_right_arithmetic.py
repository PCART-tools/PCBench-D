def shift_right_arithmetic(x: Array, y: Array) -> Array:
  r"""Elementwise arithmetic right shift: :math:`x \gg y`."""
  return shift_right_arithmetic_p.bind(x, y)
