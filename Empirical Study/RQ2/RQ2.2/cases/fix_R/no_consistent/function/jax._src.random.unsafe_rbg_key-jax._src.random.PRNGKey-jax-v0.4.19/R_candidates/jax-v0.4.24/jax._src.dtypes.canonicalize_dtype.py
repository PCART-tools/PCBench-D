@export
def canonicalize_dtype(dtype: Any, allow_extended_dtype: bool = False) -> DType | ExtendedDType:
  """Convert from a dtype to a canonical dtype based on config.x64_enabled."""
  return _canonicalize_dtype(config.enable_x64.value, allow_extended_dtype, dtype)  # pytype: disable=bad-return-type
