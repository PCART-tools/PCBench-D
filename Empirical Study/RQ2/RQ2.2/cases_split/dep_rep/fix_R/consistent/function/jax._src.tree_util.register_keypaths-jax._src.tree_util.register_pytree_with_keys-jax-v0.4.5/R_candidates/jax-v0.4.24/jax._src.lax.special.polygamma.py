def polygamma(m: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise polygamma: :math:`\psi^{(m)}(x)`."""
  return polygamma_p.bind(m, x)
