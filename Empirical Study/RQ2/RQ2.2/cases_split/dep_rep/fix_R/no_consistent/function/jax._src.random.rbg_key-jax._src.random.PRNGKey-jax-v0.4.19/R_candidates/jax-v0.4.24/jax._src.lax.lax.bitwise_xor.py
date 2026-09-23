def bitwise_xor(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise exclusive OR: :math:`x \oplus y`."""
  return xor_p.bind(x, y)
