def sin(x: ArrayLike) -> Array:
  r"""Elementwise sine: :math:`\mathrm{sin}(x)`."""
  return sin_p.bind(x)
