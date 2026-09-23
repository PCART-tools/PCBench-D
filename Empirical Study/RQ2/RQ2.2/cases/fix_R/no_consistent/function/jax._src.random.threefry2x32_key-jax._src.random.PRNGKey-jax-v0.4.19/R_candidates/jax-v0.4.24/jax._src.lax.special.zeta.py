def zeta(x: ArrayLike, q: ArrayLike) -> Array:
  r"""Elementwise Hurwitz zeta function: :math:`\zeta(x, q)`"""
  return zeta_p.bind(x, q)
