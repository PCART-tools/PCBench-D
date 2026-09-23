def complex(x: Array, y: Array) -> Array:
  r"""Elementwise make complex number: :math:`x + jy`.

  Builds a complex number from real and imaginary parts.
  """
  return complex_p.bind(x, y)
