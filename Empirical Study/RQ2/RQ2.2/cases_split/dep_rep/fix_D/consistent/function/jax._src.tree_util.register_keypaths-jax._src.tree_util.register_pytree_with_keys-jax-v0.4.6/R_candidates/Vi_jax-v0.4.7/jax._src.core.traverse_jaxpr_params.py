def traverse_jaxpr_params(f, params):
  """Applies f to each jaxpr parameter and returns a tuple of returned values."""
  return {name: f(p)
          for name, param in params.items()
          for p in (param if isinstance(param, (tuple, list)) else [param])
          if type(p) in (Jaxpr, ClosedJaxpr)}
