def rsqrt(x: ArrayLike) -> Array:
  r"""Elementwise reciprocal square root:  :math:`1 \over \sqrt{x}`."""
  return rsqrt_p.bind(x)
