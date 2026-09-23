def has_opaque_dtype(x: Any) -> bool:
  return dtypes.issubdtype(get_aval(x).dtype, dtypes.extended)
