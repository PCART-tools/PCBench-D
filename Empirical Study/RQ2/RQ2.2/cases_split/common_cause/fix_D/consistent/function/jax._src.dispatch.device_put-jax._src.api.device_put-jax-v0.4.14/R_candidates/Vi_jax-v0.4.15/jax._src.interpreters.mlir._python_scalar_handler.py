def _python_scalar_handler(dtype, val):
  return _numpy_array_constant(np.array(val, dtype))
