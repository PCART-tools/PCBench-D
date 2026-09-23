def atan(x: Array) -> Array:
  r"""Elementwise arc tangent: :math:`\mathrm{atan}(x)`."""
  return atan_p.bind(x)
