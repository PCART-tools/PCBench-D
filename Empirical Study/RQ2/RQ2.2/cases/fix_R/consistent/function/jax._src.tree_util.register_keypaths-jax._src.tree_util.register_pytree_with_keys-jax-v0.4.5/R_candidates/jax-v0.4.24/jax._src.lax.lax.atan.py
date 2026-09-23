def atan(x: ArrayLike) -> Array:
  r"""Elementwise arc tangent: :math:`\mathrm{atan}(x)`."""
  return atan_p.bind(x)
