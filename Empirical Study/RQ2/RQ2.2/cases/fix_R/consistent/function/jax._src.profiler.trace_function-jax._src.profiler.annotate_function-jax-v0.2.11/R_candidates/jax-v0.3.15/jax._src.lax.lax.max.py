def max(x: Array, y: Array) -> Array:
  r"""Elementwise maximum: :math:`\mathrm{max}(x, y)`

  For complex numbers, uses a lexicographic comparison on the
  `(real, imaginary)` pairs."""
  return max_p.bind(x, y)
