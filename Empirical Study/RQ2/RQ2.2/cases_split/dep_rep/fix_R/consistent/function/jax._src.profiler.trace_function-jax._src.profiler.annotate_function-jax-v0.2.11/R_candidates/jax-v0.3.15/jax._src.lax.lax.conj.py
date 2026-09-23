def conj(x: Array) -> Array:
  r"""Elementwise complex conjugate function: :math:`\overline{x}`."""
  return conj_p.bind(x, input_dtype=_dtype(x))
