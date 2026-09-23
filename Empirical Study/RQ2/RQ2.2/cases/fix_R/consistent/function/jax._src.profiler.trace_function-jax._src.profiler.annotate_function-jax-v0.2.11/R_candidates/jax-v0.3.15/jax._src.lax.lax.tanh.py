def tanh(x: Array) -> Array:
  r"""Elementwise hyperbolic tangent: :math:`\mathrm{tanh}(x)`."""
  return tanh_p.bind(x)
