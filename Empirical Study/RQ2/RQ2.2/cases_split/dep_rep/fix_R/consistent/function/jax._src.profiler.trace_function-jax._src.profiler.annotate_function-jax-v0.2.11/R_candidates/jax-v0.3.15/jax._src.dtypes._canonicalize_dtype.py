@functools.lru_cache(maxsize=None)
def _canonicalize_dtype(x64_enabled, dtype):
  """Convert from a dtype to a canonical dtype based on config.x64_enabled."""
  try:
    dtype = np.dtype(dtype)
  except TypeError as e:
    raise TypeError(f'dtype {dtype!r} not understood') from e

  if x64_enabled:
    return dtype
  else:
    return _dtype_to_32bit_dtype.get(dtype, dtype)
