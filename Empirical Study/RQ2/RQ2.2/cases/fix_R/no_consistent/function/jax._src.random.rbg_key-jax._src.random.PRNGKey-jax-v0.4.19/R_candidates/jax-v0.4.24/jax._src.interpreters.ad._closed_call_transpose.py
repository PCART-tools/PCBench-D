def _closed_call_transpose(params, jaxpr, args, ct, cts_in_avals, reduce_axes):
  jaxpr_, consts = jaxpr.jaxpr, jaxpr.consts
  jaxpr_ = pe.convert_constvars_jaxpr(jaxpr_)
  return call_transpose(core.closed_call_p, params, jaxpr_, (*consts, *args),
                        ct, cts_in_avals, reduce_axes)
