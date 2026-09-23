def bitwise_or(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise OR: :math:`x \vee y`."""
  return or_p.bind(x, y)
