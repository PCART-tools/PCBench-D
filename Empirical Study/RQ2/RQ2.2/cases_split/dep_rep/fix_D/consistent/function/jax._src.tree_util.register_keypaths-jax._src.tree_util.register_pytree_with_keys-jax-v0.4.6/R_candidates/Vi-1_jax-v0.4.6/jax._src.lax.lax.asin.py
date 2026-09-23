def asin(x: ArrayLike) -> Array:
  r"""Elementwise arc sine: :math:`\mathrm{asin}(x)`."""
  return asin_p.bind(x)
