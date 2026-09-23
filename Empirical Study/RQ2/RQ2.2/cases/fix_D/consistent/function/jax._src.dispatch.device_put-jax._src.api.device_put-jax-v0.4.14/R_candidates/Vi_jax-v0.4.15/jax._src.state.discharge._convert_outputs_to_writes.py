def _convert_outputs_to_writes(
    jaxpr: core.Jaxpr) -> tuple[core.Jaxpr, list[core.ShapedArray]]:
  assert not jaxpr.constvars, "Jaxpr shouldn't have constvars."

  in_avals = [v.aval for v in jaxpr.invars]
  @lu.wrap_init
  def eval_jaxpr(*refs):
    # We split the refs into the original input refs and the dummy residual
    # refs.
    orig_refs, residual_refs = split_list(refs, [len(in_avals)])
    residual_vals = core.eval_jaxpr(jaxpr, (), *orig_refs)
    for res_ref, res_val in zip(residual_refs, residual_vals):
      res_ref[...] = res_val
    return []
  res_ref_avals = [AbstractRef(v.aval) if not isinstance(v.aval, AbstractRef)
                   else v.aval for v in jaxpr.outvars]
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      eval_jaxpr, [*in_avals, *res_ref_avals])
  assert not consts
  return jaxpr, [core.ShapedArray(a.inner_aval.shape, a.inner_aval.dtype)  # pytype: disable=attribute-error
                 for a in res_ref_avals]
