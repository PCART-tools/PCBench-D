def _maybe_concretize(x: Any):
  # This is roughly the same logic as core.concrete_or_error, but we avoid
  # calling that because constructing the ConcretizationTypeError can be
  # expensive as the size of the tracing context (i.e. the jaxpr) grows.
  if isinstance(x, core.Tracer):
    if isinstance(x.aval, core.ConcreteArray):
      return x.aval.val
    else:
      return None
  return x
