@state.register_discharge_rule(cond_p)
def _cond_state_discharge_rule(in_avals, out_avals, *args, branches, linear):
  discharged_branches = tuple(
      core.ClosedJaxpr(state.discharge_state(branch.jaxpr, ())[0], ())
      for branch in branches)
  out_vals = cond_p.bind(*args, branches=discharged_branches, linear=linear)
  out_ref_vals, out_vals = util.split_list(
      out_vals, [len(out_vals) - len(out_avals)])
  ref_val_iter = iter(out_ref_vals)
  new_invals = []
  for aval in in_avals:
    new_invals.append(
        next(ref_val_iter) if isinstance(aval, state.AbstractRef) else None)
  return new_invals, out_vals
