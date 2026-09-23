def _make_closed_jaxpr(traceable: lu.WrappedFun, in_avals: Sequence[core.AbstractValue]):
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(traceable, in_avals)
  return core.ClosedJaxpr(jaxpr, consts)
