def _convert_element_type_dtype_rule(operand, *, new_dtype, weak_type):
  if operand.dtype != new_dtype:
    if (dtypes.issubdtype(operand.dtype, dtypes.extended) and
        not isinstance(operand.dtype, core.bint)):
      raise ValueError(
          f"Cannot call convert_element_type on dtype {dtype_to_string(operand.dtype)}")
    if (dtypes.issubdtype(new_dtype, dtypes.extended) and
        not isinstance(new_dtype, core.bint)):
      raise ValueError(
          f"Cannot convert_element_type to dtype={dtype_to_string(new_dtype)}")
  return new_dtype
