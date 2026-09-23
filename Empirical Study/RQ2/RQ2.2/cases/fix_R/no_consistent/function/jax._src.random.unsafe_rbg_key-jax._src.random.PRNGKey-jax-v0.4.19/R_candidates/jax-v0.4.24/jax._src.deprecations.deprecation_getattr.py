def deprecation_getattr(module, deprecations):
  def getattr(name):
    if name in deprecations:
      message, fn = deprecations[name]
      if fn is None:
        raise AttributeError(message)
      warnings.warn(message, DeprecationWarning, stacklevel=2)
      return fn
    raise AttributeError(f"module {module!r} has no attribute {name!r}")

  return getattr
