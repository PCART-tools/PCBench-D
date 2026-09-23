def _convert_inputs_to_reads(
    nsteps: int, num_res: int, jaxpr: core.Jaxpr,
    loop_invar_res: Sequence[bool]) -> core.Jaxpr:
  assert not jaxpr.constvars, "Jaxpr should not have constvars"

  @lu.wrap_init
  def eval_jaxpr(i, *refs):
    residual_refs, orig_refs = split_list(refs, [num_res])
    residual_vals = [r[()] if loop_invar else r[i] for r, loop_invar
                     in zip(residual_refs, loop_invar_res)]
    () = core.eval_jaxpr(jaxpr, (), *residual_vals, i, *orig_refs)
    return []

  res_val_avals, (i_aval,), orig_ref_avals = \
      split_list([v.aval for v in jaxpr.invars], [num_res, 1])
  res_ref_avals: list[core.AbstractValue] = [
      AbstractRef(aval) if loop_invar else  # pytype: disable=attribute-error
      AbstractRef(core.ShapedArray((nsteps, *aval.shape),  # pytype: disable=attribute-error
                  aval.dtype))  # pytype: disable=attribute-error
      for aval, loop_invar in zip(res_val_avals, loop_invar_res)]

  jaxpr, _, () = pe.trace_to_jaxpr_dynamic(
      eval_jaxpr, [i_aval, *res_ref_avals, *orig_ref_avals])
  return jaxpr
