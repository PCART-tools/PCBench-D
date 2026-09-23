def atanh(x: ArrayLike) -> Array:
  r"""Elementwise inverse hyperbolic tangent: :math:`\mathrm{atanh}(x)`."""
  return atanh_p.bind(x)
