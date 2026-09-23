def _close_jaxpr(jaxpr):
  return core.ClosedJaxpr(pe.convert_constvars_jaxpr(jaxpr), ())
