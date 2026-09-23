def clz(x: ArrayLike) -> Array:
  r"""Elementwise count-leading-zeros."""
  return clz_p.bind(x)
