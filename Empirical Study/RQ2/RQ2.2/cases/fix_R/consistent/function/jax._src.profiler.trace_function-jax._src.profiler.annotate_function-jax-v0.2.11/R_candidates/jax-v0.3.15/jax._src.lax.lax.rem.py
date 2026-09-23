def rem(x: Array, y: Array) -> Array:
  r"""Elementwise remainder: :math:`x \bmod y`."""
  return rem_p.bind(x, y)
