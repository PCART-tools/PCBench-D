def atan2(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise arc tangent of two variables:
    :math:`\mathrm{atan}({x \over y})`."""
  return atan2_p.bind(x, y)
