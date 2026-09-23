def rem(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise remainder: :math:`x \bmod y`.

  The sign of the result is taken from the dividend,
  and the absolute value of the result is always
  less than the divisor's absolute value.

  Integer division overflow
  (remainder by zero or remainder of INT_SMIN with -1)
  produces an implementation defined value.
  """
  return rem_p.bind(x, y)
