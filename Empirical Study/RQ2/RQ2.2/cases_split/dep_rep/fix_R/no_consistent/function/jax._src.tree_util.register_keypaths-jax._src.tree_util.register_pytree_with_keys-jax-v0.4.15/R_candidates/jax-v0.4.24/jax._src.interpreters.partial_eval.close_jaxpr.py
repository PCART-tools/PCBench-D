@weakref_lru_cache
def close_jaxpr(jaxpr: Jaxpr) -> ClosedJaxpr:
  return ClosedJaxpr(jaxpr, ())
