def canonicalize_dtype(dtype: Any, allow_opaque_dtype: bool = False) -> Union[DType, OpaqueDType]:
  """Convert from a dtype to a canonical dtype based on config.x64_enabled."""
  return _canonicalize_dtype(config.x64_enabled, allow_opaque_dtype, dtype)
