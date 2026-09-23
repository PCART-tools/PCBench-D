@weakref_lru_cache
def _replace_jaxpr_effects(jaxpr: ClosedJaxpr, effects: FrozenSet[Effect]):
  return jaxpr.replace(jaxpr=jaxpr.jaxpr.replace(effects=set(effects)))
