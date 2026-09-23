def le(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise less-than-or-equals: :math:`x \leq y`."""
  return le_p.bind(x, y)
