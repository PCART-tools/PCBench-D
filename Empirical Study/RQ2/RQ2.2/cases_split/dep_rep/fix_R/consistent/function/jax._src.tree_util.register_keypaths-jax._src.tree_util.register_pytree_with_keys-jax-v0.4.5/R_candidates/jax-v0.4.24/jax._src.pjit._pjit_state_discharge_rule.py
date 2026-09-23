def _pjit_state_discharge_rule(
    in_avals, out_avals, *args, jaxpr, in_shardings, out_shardings, **params):
  if not (all(map(is_unspecified, in_shardings)) and
          all(map(is_unspecified, out_shardings))): raise NotImplementedError
  jaxpr, consts = jaxpr.jaxpr, jaxpr.consts
  num_outs = len(jaxpr.outvars)
  discharged_jaxpr, discharged_consts = state_discharge.discharge_state(jaxpr, consts)
  discharged_closed_jaxpr = core.ClosedJaxpr(discharged_jaxpr, discharged_consts)
  new_in_shardings = (UnspecifiedValue(),) * len(discharged_jaxpr.invars)
  new_out_shardings = (UnspecifiedValue(),) * len(discharged_jaxpr.outvars)
  out_and_ref_vals = pjit_p.bind(
      *args, jaxpr=discharged_closed_jaxpr, in_shardings=new_in_shardings,
      out_shardings=new_out_shardings, **params)
  out_vals, ref_vals = split_list(out_and_ref_vals, [num_outs])
  ref_vals_iter = iter(ref_vals)
  new_invals = tuple(next(ref_vals_iter) if isinstance(aval, state_discharge.AbstractRef)
                     else None for aval in in_avals)
  sentinel = object()
  assert next(ref_vals_iter, sentinel) is sentinel
  return new_invals, out_vals
