def cbrt(x: Array) -> Array:
  r"""Elementwise cube root: :math:`\sqrt[3]{x}`."""
  return cbrt_p.bind(x)
