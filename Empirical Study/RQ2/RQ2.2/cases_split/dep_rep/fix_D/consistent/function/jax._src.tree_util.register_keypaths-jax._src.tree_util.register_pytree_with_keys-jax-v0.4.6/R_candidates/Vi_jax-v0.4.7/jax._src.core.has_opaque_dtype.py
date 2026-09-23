def has_opaque_dtype(x: Any) -> bool:
  return is_opaque_dtype(get_aval(x).dtype)
