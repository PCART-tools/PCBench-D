def is_opaque_dtype(dtype: Any) -> bool:
  return issubdtype(dtype, extended)
