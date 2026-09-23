def exp2(x: ArrayLike) -> Array:
  r"""Elementwise base-2 exponential: :math:`2^x`."""
  return exp2_p.bind(x)
