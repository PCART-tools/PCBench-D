def acosh(x: ArrayLike) -> Array:
  r"""Elementwise inverse hyperbolic cosine: :math:`\mathrm{acosh}(x)`."""
  return acosh_p.bind(x)
