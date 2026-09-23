def reciprocal(x: ArrayLike) -> Array:
  r"""Elementwise reciprocal: :math:`1 \over x`."""
  return integer_pow(x, -1)
