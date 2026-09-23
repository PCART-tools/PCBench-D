def tan(x: ArrayLike) -> Array:
  r"""Elementwise tangent: :math:`\mathrm{tan}(x)`."""
  return tan_p.bind(x)
