@lu.cache
def _pjit_transpose_trace(fun, in_avals):
  transpose_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun, in_avals)
  transpose_jaxpr = core.ClosedJaxpr(transpose_jaxpr, consts)
  return transpose_jaxpr
