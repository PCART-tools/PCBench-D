def reduce_precision(operand: Union[float, Array],
                     exponent_bits: int,
                     mantissa_bits: int) -> Array:
  """Wraps XLA's `ReducePrecision
  <https://www.tensorflow.org/xla/operation_semantics#reduceprecision>`_
  operator.
  """
  exponent_bits = core.concrete_or_error(
    operator.index, exponent_bits, "exponent_bits argument of lax.reduce_precision")
  mantissa_bits = core.concrete_or_error(
    operator.index, mantissa_bits, "mantissa_bits argument of lax.reduce_precision")
  return reduce_precision_p.bind(operand, exponent_bits=exponent_bits, mantissa_bits=mantissa_bits)
