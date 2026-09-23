def rev(operand: Array, dimensions: Sequence[int]) -> Array:
  """Wraps XLA's `Rev
  <https://www.tensorflow.org/xla/operation_semantics#rev_reverse>`_
  operator.
  """
  return rev_p.bind(operand, dimensions=tuple(dimensions))
