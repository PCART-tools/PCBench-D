def le(x: Array, y: Array) -> Array:
  r"""Elementwise less-than-or-equals: :math:`x \leq y`."""
  return le_p.bind(x, y)
