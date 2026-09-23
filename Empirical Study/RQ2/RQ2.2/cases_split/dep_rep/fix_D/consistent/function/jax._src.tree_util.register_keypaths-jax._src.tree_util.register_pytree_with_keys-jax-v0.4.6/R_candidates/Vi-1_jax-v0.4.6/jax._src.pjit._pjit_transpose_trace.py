@lu.cache
def _pjit_transpose_trace(fun, in_avals, api_name):
  transpose_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      fun, in_avals, debug_info=pe.debug_info_final(fun, api_name))
  transpose_jaxpr = core.ClosedJaxpr(transpose_jaxpr, consts)
  return transpose_jaxpr
