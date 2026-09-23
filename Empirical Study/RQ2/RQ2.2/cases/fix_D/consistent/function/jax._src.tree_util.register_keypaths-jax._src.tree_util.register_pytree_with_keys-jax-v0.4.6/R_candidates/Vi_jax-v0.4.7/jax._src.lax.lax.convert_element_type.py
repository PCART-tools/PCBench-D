def convert_element_type(operand: ArrayLike, new_dtype: DTypeLike) -> Array:
  """Elementwise cast.

  Wraps XLA's `ConvertElementType
  <https://www.tensorflow.org/xla/operation_semantics#convertelementtype>`_
  operator, which performs an elementwise conversion from one type to another.
  Similar to a C++ `static_cast`.

  Args:
    operand: an array or scalar value to be cast
    new_dtype: a NumPy dtype representing the target type.

  Returns:
    An array with the same shape as `operand`, cast elementwise to `new_dtype`.
  """
  if hasattr(operand, '__jax_array__'):
    operand = operand.__jax_array__()  # type: ignore
  return _convert_element_type(operand, new_dtype, weak_type=False)
