def conj(x: ArrayLike) -> Array:
  r"""Elementwise complex conjugate function: :math:`\overline{x}`."""
  # TODO(mattjj): remove input_dtype, not needed anymore
  return conj_p.bind(x, input_dtype=_dtype(x))
