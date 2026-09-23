def _device_get(x):
  if isinstance(x, core.Tracer):
    return x
  try:
    toarray = x.__array__
  except AttributeError:
    return x
  else:
    return toarray()
