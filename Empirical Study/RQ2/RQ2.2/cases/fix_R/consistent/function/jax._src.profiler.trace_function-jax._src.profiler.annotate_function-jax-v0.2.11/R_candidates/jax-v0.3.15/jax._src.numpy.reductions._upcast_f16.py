def _upcast_f16(dtype):
  if dtype in [np.float16, dtypes.bfloat16]:
    return np.dtype('float32')
  return dtype
