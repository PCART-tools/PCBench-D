def acosh(x: Array) -> Array:
  r"""Elementwise inverse hyperbolic cosine: :math:`\mathrm{acosh}(x)`."""
  return acosh_p.bind(x)
