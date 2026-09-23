def asinh(x: ArrayLike) -> Array:
  r"""Elementwise inverse hyperbolic sine: :math:`\mathrm{asinh}(x)`."""
  return asinh_p.bind(x)
