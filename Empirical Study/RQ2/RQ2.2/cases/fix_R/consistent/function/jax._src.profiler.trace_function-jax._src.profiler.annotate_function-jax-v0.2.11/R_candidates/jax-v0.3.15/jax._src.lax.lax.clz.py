def clz(x: Array) -> Array:
  r"""Elementwise count-leading-zeros."""
  return clz_p.bind(x)
