def checkify_fun_to_jaxpr(f, error, enabled_errors, in_avals):
  f, msgs = checkify_subtrace(f)
  f = checkify_traceable(f, tuple(error.msgs.items()), enabled_errors)
  err_aval = core.raise_to_shaped(core.get_aval(error.err))
  code_aval = core.raise_to_shaped(core.get_aval(error.code))
  payload_aval = core.raise_to_shaped(core.get_aval(error.payload))
  avals_in = [err_aval, code_aval, payload_aval, *in_avals]
  jaxpr_out, _, literals_out = pe.trace_to_jaxpr_dynamic(f, avals_in)
  return core.ClosedJaxpr(jaxpr_out, literals_out), msgs()
