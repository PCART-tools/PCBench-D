def ceil(x: Array) -> Array:
  r"""Elementwise ceiling: :math:`\left\lceil x \right\rceil`."""
  return ceil_p.bind(x)
