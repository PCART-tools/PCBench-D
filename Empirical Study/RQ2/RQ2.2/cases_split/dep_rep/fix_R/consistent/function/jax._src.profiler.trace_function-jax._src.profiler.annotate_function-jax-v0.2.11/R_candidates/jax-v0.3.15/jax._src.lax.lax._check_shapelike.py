def _check_shapelike(fun_name, arg_name, obj, non_zero_shape=False):
  """Check that `obj` is a shape-like value (e.g. tuple of nonnegative ints)."""
  if not isinstance(obj, (tuple, list, np.ndarray)):
    msg = "{} {} must be of type tuple/list/ndarray, got {}."
    raise TypeError(msg.format(fun_name, arg_name, type(obj)))
  # bool(obj) for an ndarray raises an error, so we check len
  if not len(obj):  # pylint: disable=g-explicit-length-test
    return
  if (config.jax_dynamic_shapes and isinstance(obj, (tuple, list)) and
      any(isinstance(d, (core.Tracer, core.BInt)) for d in obj)):
    return  # TODO(mattjj): handle more checks in the dynamic shape case
  obj_arr = np.array(obj)
  if obj_arr.ndim != 1:
    msg = "{} {} must be 1-dimensional, got {}."
    raise TypeError(msg.format(obj_arr.ndim))
  try:
    canonicalize_shape(obj_arr)
  except TypeError as err:
    msg = "{} {} must have every element be an integer type, got {}."
    raise TypeError(msg.format(fun_name, arg_name, tuple(map(type, obj)))) from err
  lower_bound, bound_error = (
      (1, "strictly positive") if non_zero_shape else (0, "nonnegative"))
  if not all(core.greater_equal_dim(d, lower_bound) for d in obj_arr):
    msg = "{} {} must have every element be {}, got {}."
    raise TypeError(msg.format(fun_name, arg_name, bound_error, obj))
