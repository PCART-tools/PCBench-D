def complex(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise make complex number: :math:`x + jy`.

  Builds a complex number from real and imaginary parts.
  """
  return complex_p.bind(x, y)
