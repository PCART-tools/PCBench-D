def bitcast_convert_type(operand: Array, new_dtype: DType) -> Array:
  """Elementwise bitcast.

  Wraps XLA's `BitcastConvertType
  <https://www.tensorflow.org/xla/operation_semantics#bitcastconverttype>`_
  operator, which performs a bit cast from one type to another. The bitwidth
  of the source and destination types must match.

  Args:
    operand: an array or scalar value to be cast
    new_dtype: the new type. Should be a NumPy type.

  Returns:
    An array with the same shape as `operand`, bitcast elementwise to
    `new_dtype`.
  """
  new_dtype = dtypes.canonicalize_dtype(new_dtype)
  return bitcast_convert_type_p.bind(operand, new_dtype=new_dtype)
