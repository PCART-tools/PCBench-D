def canonicalize_dtype(dtype):
  return _canonicalize_dtype(config.x64_enabled, dtype)
