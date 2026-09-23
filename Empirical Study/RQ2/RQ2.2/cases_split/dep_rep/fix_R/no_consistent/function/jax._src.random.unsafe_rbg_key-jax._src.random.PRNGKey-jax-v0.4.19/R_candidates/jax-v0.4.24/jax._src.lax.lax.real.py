def real(x: ArrayLike) -> Array:
  r"""Elementwise extract real part: :math:`\mathrm{Re}(x)`.

  Returns the real part of a complex number.
  """
  return real_p.bind(x)
