def is_opaque_dtype(dtype: Any) -> bool:
  return type(dtype) in opaque_dtypes
