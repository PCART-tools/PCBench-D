def cbrt(x: ArrayLike) -> Array:
  r"""Elementwise cube root: :math:`\sqrt[3]{x}`."""
  return cbrt_p.bind(x)
