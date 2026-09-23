def cos(x: ArrayLike) -> Array:
  r"""Elementwise cosine: :math:`\mathrm{cos}(x)`."""
  return cos_p.bind(x)
