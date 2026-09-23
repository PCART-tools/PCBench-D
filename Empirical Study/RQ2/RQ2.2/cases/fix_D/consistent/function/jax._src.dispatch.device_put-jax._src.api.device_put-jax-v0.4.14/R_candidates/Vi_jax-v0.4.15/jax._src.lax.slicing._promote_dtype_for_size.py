def _promote_dtype_for_size(dtype, size):
  if not dtypes.issubdtype(dtype, np.integer):
    return dtype
  # size may be a dynamic shape, in which case we return at least int32
  try:
    size = int(size)
  except:
    return dtype if np.iinfo(dtype).bits >= 32 else np.dtype('int32')
  if size <= np.iinfo(dtype).max:
    return dtype
  elif size <= np.iinfo(np.int32).max:
    return np.dtype('int32')
  else:
    return dtypes.canonicalize_dtype(np.int64)
