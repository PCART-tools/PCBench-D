def floor(x: ArrayLike) -> Array:
  r"""Elementwise floor: :math:`\left\lfloor x \right\rfloor`."""
  return floor_p.bind(x)
