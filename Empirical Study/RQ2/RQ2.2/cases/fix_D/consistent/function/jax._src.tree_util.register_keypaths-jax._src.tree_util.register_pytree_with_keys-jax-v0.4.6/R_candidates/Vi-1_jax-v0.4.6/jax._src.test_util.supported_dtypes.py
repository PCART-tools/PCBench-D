def supported_dtypes():
  if device_under_test() == "tpu":
    types = {np.bool_, np.int8, np.int16, np.int32, np.uint8, np.uint16,
             np.uint32, _dtypes.bfloat16, np.float16, np.float32, np.complex64}
  elif device_under_test() == "iree":
    types = {np.bool_, np.int8, np.int16, np.int32, np.uint8, np.uint16,
             np.uint32, np.float32}
  else:
    types = {np.bool_, np.int8, np.int16, np.int32, np.int64,
             np.uint8, np.uint16, np.uint32, np.uint64,
             _dtypes.bfloat16, np.float16, np.float32, np.float64,
             np.complex64, np.complex128}
  if not config.x64_enabled:
    types -= {np.uint64, np.int64, np.float64, np.complex128}
  return types
