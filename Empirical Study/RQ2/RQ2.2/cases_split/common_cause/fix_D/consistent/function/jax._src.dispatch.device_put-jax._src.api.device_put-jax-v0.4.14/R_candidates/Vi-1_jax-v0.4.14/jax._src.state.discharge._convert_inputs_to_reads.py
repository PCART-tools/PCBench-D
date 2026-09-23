def _convert_inputs_to_reads(num_res: int, jaxpr: core.Jaxpr) -> core.Jaxpr:
  assert not jaxpr.constvars, "Jaxpr should not have constvars"

  @lu.wrap_init
  def eval_jaxpr(*refs):
    residual_refs, orig_refs = split_list(refs, [num_res])
    residual_vals = [r[...] for r in residual_refs]
    () = core.eval_jaxpr(jaxpr, (), *residual_vals, *orig_refs)
    return []

  res_val_avals, orig_ref_avals = \
      split_list([v.aval for v in jaxpr.invars], [num_res])
  res_ref_avals = [AbstractRef(aval) if not isinstance(aval, AbstractRef) else
                   aval for aval in res_val_avals]
  jaxpr, _, () = pe.trace_to_jaxpr_dynamic(
      eval_jaxpr, [*res_ref_avals, *orig_ref_avals])
  return jaxpr
