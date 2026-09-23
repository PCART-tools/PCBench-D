def transpose(operand: Array, permutation: Sequence[int]) -> Array:
  """Wraps XLA's `Transpose
  <https://www.tensorflow.org/xla/operation_semantics#transpose>`_
  operator.
  """
  permutation = tuple(operator.index(d) for d in permutation)
  if (permutation == tuple(range(np.ndim(operand)))
      and isinstance(operand, (core.Tracer, device_array.DeviceArray))):
    return operand
  else:
    return transpose_p.bind(operand, permutation=permutation)
