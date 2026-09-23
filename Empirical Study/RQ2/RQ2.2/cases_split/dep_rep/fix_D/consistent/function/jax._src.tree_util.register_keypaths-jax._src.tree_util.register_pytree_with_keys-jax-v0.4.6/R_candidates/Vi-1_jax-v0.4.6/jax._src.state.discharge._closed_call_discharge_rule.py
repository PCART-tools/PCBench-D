@register_discharge_rule(core.closed_call_p)
def _closed_call_discharge_rule(
    in_avals: Sequence[core.AbstractValue], _,*args,
    call_jaxpr: core.ClosedJaxpr):
  jaxpr, consts = call_jaxpr.jaxpr, call_jaxpr.consts
  num_outs = len(jaxpr.outvars)
  discharged_jaxpr, discharged_consts = discharge_state(jaxpr, consts)
  discharged_closed_jaxpr = core.ClosedJaxpr(discharged_jaxpr,
                                             discharged_consts)
  fun = lu.wrap_init(core.jaxpr_as_fun(discharged_closed_jaxpr))
  out_and_ref_vals = core.closed_call_p.bind(fun, *args,
                                             call_jaxpr=discharged_closed_jaxpr)
  out_vals, ref_vals = split_list(out_and_ref_vals, [num_outs])
  ref_vals_iter = iter(ref_vals)
  new_invals = tuple(next(ref_vals_iter) if isinstance(aval, AbstractRef)
                     else None for aval in in_avals)
  assert next(ref_vals_iter, None) is None
  return new_invals, out_vals
