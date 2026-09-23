def _wrap_numpy_nullary_function(f):
  """Adapts `f` to return a DeviceArray instead of an np.ndarray.

  `f` cannot have any non-static array arguments.
  """
  @_wraps(f, update_doc=False)
  def wrapper(*args, **kwargs):
    args = [core.concrete_or_error(None, arg, f"the error occurred in argument {i} jnp.{f.__name__}()")
            for i, arg in enumerate(args)]
    kwargs = {key: core.concrete_or_error(None, val, f"the error occurred in argument '{key}' jnp.{f.__name__}()")
              for key, val in kwargs.items()}
    return asarray(f(*args, **kwargs))
  return wrapper
