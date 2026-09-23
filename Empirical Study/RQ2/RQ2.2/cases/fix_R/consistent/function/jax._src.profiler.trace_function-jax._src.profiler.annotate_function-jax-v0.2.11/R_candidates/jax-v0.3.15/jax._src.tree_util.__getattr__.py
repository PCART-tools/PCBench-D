def __getattr__(name):
  prefix = "_deprecated_"
  if name.startswith(prefix):
    name = name[len(prefix):]
    return _deprecate(globals()[name])
  else:
    raise AttributeError(f"module {__name__} has no attribute {name!r}")
