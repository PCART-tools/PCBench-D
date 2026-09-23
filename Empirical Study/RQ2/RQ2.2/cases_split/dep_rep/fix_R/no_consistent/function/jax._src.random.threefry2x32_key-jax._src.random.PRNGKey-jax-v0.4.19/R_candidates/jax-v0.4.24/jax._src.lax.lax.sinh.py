def sinh(x: ArrayLike) -> Array:
  r"""Elementwise hyperbolic sine: :math:`\mathrm{sinh}(x)`."""
  return sinh_p.bind(x)
