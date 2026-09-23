def _device_array_constant_handler(val, canonicalize_types):
  return _ndarray_constant_handler(np.asarray(val.device_buffer),
                                   canonicalize_types)
