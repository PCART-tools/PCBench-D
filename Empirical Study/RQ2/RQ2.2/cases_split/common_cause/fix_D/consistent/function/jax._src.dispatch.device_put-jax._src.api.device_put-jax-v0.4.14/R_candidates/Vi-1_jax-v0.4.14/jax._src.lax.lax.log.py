def log(x: ArrayLike) -> Array:
  r"""Elementwise natural logarithm: :math:`\mathrm{log}(x)`."""
  return log_p.bind(x)
