def collapse(operand: Array, start_dimension: int,
             stop_dimension: int) -> Array:
  """Collapses dimensions of an array into a single dimension.

  For example, if ``operand`` is an array with shape ``[2, 3, 4]``,
  ``collapse(operand, 0, 2).shape == [6, 4]``. The elements of the collapsed
  dimension are laid out major-to-minor, i.e., with the lowest-numbered
  dimension as the slowest varying dimension.

  Args:
    operand: an input array.
    start_dimension: the start of the dimensions to collapse (inclusive).
    stop_dimension: the end of the dimensions to collapse (exclusive).

  Returns:
    An array where dimensions ``[start_dimension, stop_dimension)`` have been
    collapsed (raveled) into a single dimension.
  """
  lo, hi = start_dimension, stop_dimension
  size = prod(operand.shape[lo:hi])
  new_shape = operand.shape[:lo] + (size,) + operand.shape[hi:]
  return reshape(operand, new_shape)
