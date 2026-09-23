def _resolve_kwargs(fun, args, kwargs):
  if isinstance(fun, partial):
    # functools.partial should have an opaque signature.
    fun = lambda *args, **kwargs: None
  ba = inspect.signature(fun).bind(*args, **kwargs)
  ba.apply_defaults()
  if ba.kwargs:
    raise TypeError("keyword arguments could not be resolved to positions")
  else:
    return ba.args
