def round(x: ArrayLike,
          rounding_method: RoundingMethod = RoundingMethod.AWAY_FROM_ZERO
          ) -> Array:
  r"""Elementwise round.

  Rounds values to the nearest integer.

  Args:
    x: an array or scalar value to round.
    rounding_method: the method to use when rounding halfway values
      (e.g., `0.5`). See ``lax.RoundingMethod`` for the list of possible
      values.

  Returns:
    An array containing the elementwise rounding of x.
  """
  rounding_method = RoundingMethod(rounding_method)
  return round_p.bind(x, rounding_method=rounding_method)
