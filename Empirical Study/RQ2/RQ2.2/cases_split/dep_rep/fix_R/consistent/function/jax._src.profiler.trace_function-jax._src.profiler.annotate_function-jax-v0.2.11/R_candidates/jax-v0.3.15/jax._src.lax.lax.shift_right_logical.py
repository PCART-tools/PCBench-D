def shift_right_logical(x: Array, y: Array) -> Array:
  r"""Elementwise logical right shift: :math:`x \gg y`."""
  return shift_right_logical_p.bind(x, y)
