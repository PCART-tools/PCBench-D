def _dot_general_dtype_rule(lhs, rhs, *, dimension_numbers, precision,
                            preferred_element_type: Optional[DTypeLike]):
  input_dtype = naryop_dtype_rule(_input_dtype, [_any, _any], 'dot_general', lhs, rhs)
  if preferred_element_type is None:
    return input_dtype
  _validate_preferred_element_type(input_dtype, preferred_element_type)
  return preferred_element_type
