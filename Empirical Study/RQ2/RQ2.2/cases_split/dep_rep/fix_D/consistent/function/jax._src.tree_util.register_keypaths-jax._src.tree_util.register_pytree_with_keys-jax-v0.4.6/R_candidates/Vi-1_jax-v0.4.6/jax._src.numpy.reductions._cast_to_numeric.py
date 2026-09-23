def _cast_to_numeric(operand: ArrayLike) -> Array:
  return _promote_dtypes_numeric(operand)[0]
