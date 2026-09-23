def bitwise_and(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise AND: :math:`x \wedge y`."""
  return and_p.bind(x, y)
