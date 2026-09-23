@weakref_lru_cache
def _cached_scan_pad_jaxpr(jaxpr):
  return core.ClosedJaxpr(*pe.pad_jaxpr(jaxpr.jaxpr, jaxpr.consts))
