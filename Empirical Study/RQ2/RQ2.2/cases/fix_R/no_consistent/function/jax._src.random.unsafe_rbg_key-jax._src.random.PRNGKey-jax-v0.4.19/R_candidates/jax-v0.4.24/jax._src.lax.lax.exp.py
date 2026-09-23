def exp(x: ArrayLike) -> Array:
  r"""Elementwise exponential: :math:`e^x`."""
  return exp_p.bind(x)
