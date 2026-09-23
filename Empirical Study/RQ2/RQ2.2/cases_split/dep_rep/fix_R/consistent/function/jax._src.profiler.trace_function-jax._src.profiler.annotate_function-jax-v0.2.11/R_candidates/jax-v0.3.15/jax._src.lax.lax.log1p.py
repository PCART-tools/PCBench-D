def log1p(x: Array) -> Array:
  r"""Elementwise :math:`\mathrm{log}(1 + x)`."""
  return log1p_p.bind(x)
