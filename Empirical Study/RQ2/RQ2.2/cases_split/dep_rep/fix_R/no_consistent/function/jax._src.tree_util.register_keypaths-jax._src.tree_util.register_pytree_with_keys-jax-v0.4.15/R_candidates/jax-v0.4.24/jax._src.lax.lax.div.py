def div(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise division: :math:`x \over y`.

  Integer division overflow
  (division by zero or signed division of INT_SMIN with -1)
  produces an implementation defined value.
  """
  return div_p.bind(x, y)
