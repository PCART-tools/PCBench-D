def transpose(operand: ArrayLike,
              permutation: Sequence[int] | np.ndarray) -> Array:
  """Wraps XLA's `Transpose
  <https://www.tensorflow.org/xla/operation_semantics#transpose>`_
  operator.
  """
  permutation = tuple(operator.index(d) for d in permutation)
  if permutation == tuple(range(np.ndim(operand))) and isinstance(operand, Array):
    return type_cast(Array, operand)
  else:
    return transpose_p.bind(operand, permutation=permutation)
