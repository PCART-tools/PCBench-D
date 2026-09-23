def logistic(x: ArrayLike) -> Array:
  r"""Elementwise logistic (sigmoid) function: :math:`\frac{1}{1 + e^{-x}}`."""
  return logistic_p.bind(x)
