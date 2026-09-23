def bitcast_convert_type(operand: ArrayLike, new_dtype: DTypeLike) -> Array:
  """Elementwise bitcast.

  Wraps XLA's `BitcastConvertType
  <https://www.tensorflow.org/xla/operation_semantics#bitcastconverttype>`_
  operator, which performs a bit cast from one type to another.

  The output shape depends on the size of the input and output dtypes with
  the following logic::

    if new_dtype.itemsize == operand.dtype.itemsize:
      output_shape = operand.shape
    if new_dtype.itemsize < operand.dtype.itemsize:
      output_shape = (*operand.shape, operand.dtype.itemsize // new_dtype.itemsize)
    if new_dtype.itemsize > operand.dtype.itemsize:
      assert operand.shape[-1] * operand.dtype.itemsize == new_dtype.itemsize
      output_shape = operand.shape[:-1]

  Args:
    operand: an array or scalar value to be cast
    new_dtype: the new type. Should be a NumPy type.

  Returns:
    An array of shape `output_shape` (see above) and type `new_dtype`,
    constructed from the same bits as operand.
  """
  new_dtype = dtypes.canonicalize_dtype(new_dtype)
  return bitcast_convert_type_p.bind(operand, new_dtype=new_dtype)
