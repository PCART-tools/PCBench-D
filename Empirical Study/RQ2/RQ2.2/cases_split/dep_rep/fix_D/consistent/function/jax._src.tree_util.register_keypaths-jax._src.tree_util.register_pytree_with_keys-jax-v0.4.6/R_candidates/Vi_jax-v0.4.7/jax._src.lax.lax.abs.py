def abs(x: ArrayLike) -> Array:
  r"""Elementwise absolute value: :math:`|x|`."""
  return abs_p.bind(x)
