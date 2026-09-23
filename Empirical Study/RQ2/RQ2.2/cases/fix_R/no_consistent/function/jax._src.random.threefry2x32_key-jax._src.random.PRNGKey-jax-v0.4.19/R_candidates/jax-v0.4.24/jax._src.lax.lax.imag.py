def imag(x: ArrayLike) -> Array:
  r"""Elementwise extract imaginary part: :math:`\mathrm{Im}(x)`.

  Returns the imaginary part of a complex number.
  """
  return imag_p.bind(x)
