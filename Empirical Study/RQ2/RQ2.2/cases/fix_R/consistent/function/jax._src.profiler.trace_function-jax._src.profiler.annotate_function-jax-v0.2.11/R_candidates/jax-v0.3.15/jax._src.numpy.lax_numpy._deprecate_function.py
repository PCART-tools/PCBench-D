def _deprecate_function(fun, msg):
  @functools_wraps(fun)
  def wrapped(*args, **kwargs):
    warnings.warn(msg, FutureWarning)
    return fun(*args, **kwargs)
  return wrapped
