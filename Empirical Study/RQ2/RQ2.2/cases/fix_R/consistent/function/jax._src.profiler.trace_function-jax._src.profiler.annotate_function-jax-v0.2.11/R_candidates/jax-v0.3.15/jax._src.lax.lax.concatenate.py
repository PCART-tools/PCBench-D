def concatenate(operands: Sequence[Array], dimension: int) -> Array:
  """Concatenates a sequence of arrays along `dimension`.

  Wraps XLA's `Concatenate
  <https://www.tensorflow.org/xla/operation_semantics#concatenate>`_
  operator.

  Args:
    operands: a sequence of arrays to concatenate. The arrays must have equal
      shapes, except in the `dimension` axis.
    dimension: the dimension along which to concatenate the arrays.

  Returns:
    An array containing the concatenation.
  """
  if len(operands) == 0:
    raise ValueError("concatenate requires a non-empty sequences of arrays")
  return concatenate_p.bind(*operands, dimension=dimension)
