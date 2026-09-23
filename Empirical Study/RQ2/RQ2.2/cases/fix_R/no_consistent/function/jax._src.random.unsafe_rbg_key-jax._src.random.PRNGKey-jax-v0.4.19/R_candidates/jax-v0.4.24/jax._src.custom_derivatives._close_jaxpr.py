def _close_jaxpr(jaxpr):
  return pe.close_jaxpr(pe.convert_constvars_jaxpr(jaxpr))
