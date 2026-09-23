def concrete_or_error(force: Any, val: Any, context=""):
  """Like force(val), but gives the context in the error message."""
  if force is None:
    force = lambda x: x
  if isinstance(val, Tracer):
    if isinstance(val.aval, ConcreteArray):
      return force(val.aval.val)
    else:
      raise ConcretizationTypeError(val, context)
  else:
    return force(val)
