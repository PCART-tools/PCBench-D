@weakref_lru_cache
def _cached_closed_jaxpr_discharge(closed_jaxpr):
  jaxpr, consts = closed_jaxpr.jaxpr, closed_jaxpr.consts
  num_outs = len(jaxpr.outvars)
  discharged_jaxpr, discharged_consts = discharge_state(jaxpr, consts)
  discharged_closed_jaxpr = core.ClosedJaxpr(discharged_jaxpr, discharged_consts)
  fun = lu.wrap_init(core.jaxpr_as_fun(discharged_closed_jaxpr))
  return discharged_closed_jaxpr, num_outs, fun
