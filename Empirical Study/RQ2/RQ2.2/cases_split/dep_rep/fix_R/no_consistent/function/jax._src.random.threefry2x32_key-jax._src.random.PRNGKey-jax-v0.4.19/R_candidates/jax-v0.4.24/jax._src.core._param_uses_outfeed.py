def _param_uses_outfeed(param):
  if type(param) is Jaxpr:
    if jaxpr_uses_outfeed(param):
      return True
  elif type(param) is ClosedJaxpr:
    if jaxpr_uses_outfeed(param.jaxpr):
      return True
  return False
