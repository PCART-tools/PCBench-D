def cosh(x: ArrayLike) -> Array:
  r"""Elementwise hyperbolic cosine: :math:`\mathrm{cosh}(x)`."""
  return cosh_p.bind(x)
