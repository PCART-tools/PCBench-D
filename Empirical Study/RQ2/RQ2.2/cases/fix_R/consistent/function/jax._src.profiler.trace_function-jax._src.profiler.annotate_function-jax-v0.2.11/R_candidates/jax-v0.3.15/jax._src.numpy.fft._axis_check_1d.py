def _axis_check_1d(func_name, axis):
  full_name = "jax.numpy.fft." + func_name
  if isinstance(axis, (list, tuple)):
    raise ValueError(
        "%s does not support multiple axes. Please use %sn. "
        "Got axis = %r." % (full_name, full_name, axis)
    )
