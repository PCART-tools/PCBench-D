def min(x: Array, y: Array) -> Array:
  r"""Elementwise minimum:  :math:`\mathrm{min}(x, y)`

  For complex numbers, uses a lexicographic comparison on the
  `(real, imaginary)` pairs."""
  return min_p.bind(x, y)
