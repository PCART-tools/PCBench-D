def _initial_style_jaxpr(fun, in_avals):
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun, in_avals)
  return jaxpr, consts
