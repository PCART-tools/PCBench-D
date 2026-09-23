@weakref_lru_cache
def _cached_for_jaxpr(jaxpr):
  discharged_jaxpr, body_consts = discharge_state(jaxpr, ())
  return core.ClosedJaxpr(discharged_jaxpr, body_consts)
