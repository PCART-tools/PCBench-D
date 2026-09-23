def _convert_element_type_dtype_rule(operand, *, new_dtype, weak_type):
  if (operand.dtype != new_dtype and
      ((dtypes.issubdtype(operand.dtype, dtypes.extended) and
        not operand.dtype._rules.convert_from(operand.dtype, new_dtype)) or  # type: ignore
       (dtypes.issubdtype(new_dtype, dtypes.extended) and
        not new_dtype._rules.convert_to(operand.dtype, new_dtype)))):  # type: ignore
    raise ValueError(
        f"Cannot convert_element_type from {dtype_to_string(operand.dtype)} "
        f"to {dtype_to_string(new_dtype)}")
  return new_dtype
