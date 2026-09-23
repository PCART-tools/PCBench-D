def canonicalize_dtype(dtype: Any, allow_extended_dtype: bool = False, allow_opaque_dtype: Any = None) -> Union[DType, ExtendedDType]:
  """Convert from a dtype to a canonical dtype based on config.x64_enabled."""
  if allow_opaque_dtype is not None:
    # TODO(jakevdp): complete the deprecation cycle (Deprecated July 24 2023).
    warnings.warn(
      "allow_opaque_dtype argument is deprecated; use allow_extended_dtype.",
      DeprecationWarning)
    allow_extended_dtype = allow_opaque_dtype
  return _canonicalize_dtype(config.x64_enabled, allow_extended_dtype, dtype)  # type: ignore[bad-return-type]
