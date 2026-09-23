def _original_func(f):
  if isinstance(f, property):
    return cast(property, f).fget
  elif isinstance(f, functools.cached_property):
    return f.func
  return f
