def bitwise_xor(x: Array, y: Array) -> Array:
  r"""Elementwise exclusive OR: :math:`x \oplus y`."""
  return xor_p.bind(x, y)
