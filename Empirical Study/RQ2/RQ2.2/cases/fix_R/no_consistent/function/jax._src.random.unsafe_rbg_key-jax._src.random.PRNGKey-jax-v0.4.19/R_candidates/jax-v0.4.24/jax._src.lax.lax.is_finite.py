def is_finite(x: ArrayLike) -> Array:
  r"""Elementwise :math:`\mathrm{isfinite}`.

  For each element x returns `True` if and only if x is not :math:`\pm\infty` or
  :math:`\mathit{NaN}`.
  """
  return is_finite_p.bind(x)
