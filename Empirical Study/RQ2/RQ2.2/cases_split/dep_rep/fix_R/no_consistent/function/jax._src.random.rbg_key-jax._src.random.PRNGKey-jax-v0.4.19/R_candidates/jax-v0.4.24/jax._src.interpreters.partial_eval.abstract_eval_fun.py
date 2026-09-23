def abstract_eval_fun(fun, *avals, debug_info=None, **params):
  _, avals_out, _, () = trace_to_jaxpr_dynamic(
      lu.wrap_init(fun, params), avals, debug_info)
  assert all(isinstance(aval, AbstractValue) for aval in avals_out)
  return avals_out
