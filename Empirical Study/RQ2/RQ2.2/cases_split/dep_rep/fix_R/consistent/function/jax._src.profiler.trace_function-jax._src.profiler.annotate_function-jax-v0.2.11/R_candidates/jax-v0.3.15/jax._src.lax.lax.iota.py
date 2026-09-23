def iota(dtype: DType, size: int) -> Array:
  """Wraps XLA's `Iota
  <https://www.tensorflow.org/xla/operation_semantics#iota>`_
  operator.
  """
  return broadcasted_iota(dtype, (size,), 0)
