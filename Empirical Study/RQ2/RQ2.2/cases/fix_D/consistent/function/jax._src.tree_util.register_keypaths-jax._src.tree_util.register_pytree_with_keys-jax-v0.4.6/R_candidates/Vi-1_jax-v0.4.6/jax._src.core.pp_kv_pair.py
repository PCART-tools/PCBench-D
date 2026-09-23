def pp_kv_pair(k:str, v: Any, context: JaxprPpContext, settings: JaxprPpSettings) -> pp.Doc:
  if type(v) is tuple and all(isinstance(j, (Jaxpr, ClosedJaxpr)) for j in v):
    pp_v = pp_jaxprs(v, context, settings)
  elif isinstance(v, Jaxpr):
    pp_v = pp_jaxpr(v, context, settings)
  elif isinstance(v, ClosedJaxpr):
    pp_v = pp_jaxpr(v.jaxpr, context, settings)
  else:
    pp_v = pp.text(str(v))
  return pp.text(f'{k}=') + pp_v
