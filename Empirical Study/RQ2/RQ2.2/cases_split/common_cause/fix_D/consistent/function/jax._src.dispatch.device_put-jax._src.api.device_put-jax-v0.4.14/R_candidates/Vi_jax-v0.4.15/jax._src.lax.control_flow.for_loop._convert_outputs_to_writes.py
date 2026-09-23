def _convert_outputs_to_writes(
    nsteps: int, jaxpr: core.Jaxpr, loop_invar_res: Sequence[bool]
    ) -> tuple[core.Jaxpr, list[core.ShapedArray]]:
  assert not jaxpr.constvars, "Jaxpr shouldn't have constvars."

  in_avals = [v.aval for v in jaxpr.invars]  # [i, *orig_ref_avals]
  @lu.wrap_init
  def eval_jaxpr(i, *refs):
    # We split the refs into the original input refs and the dummy residual
    # refs.
    orig_refs, residual_refs = split_list(refs, [len(in_avals) - 1])
    residual_vals = core.eval_jaxpr(jaxpr, (), i, *orig_refs)
    for res_ref, res_val, loop_invar in zip(residual_refs, residual_vals,
                                            loop_invar_res):
      if loop_invar:
        res_ref[()] = res_val
      else:
        res_ref[i] = res_val
    return []
  # TODO(mattjj, sharadmv): better handling of tokens, which don't have shape/dtype
  res_ref_avals: list[core.AbstractValue] = [
      AbstractRef(v.aval) if loop_invar else  # pytype: disable=attribute-error
      AbstractRef(core.ShapedArray((nsteps, *v.aval.shape),  # pytype: disable=attribute-error
                  v.aval.dtype))  # pytype: disable=attribute-error
      for v, loop_invar in zip(jaxpr.outvars, loop_invar_res)]
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      eval_jaxpr, [*in_avals, *res_ref_avals])
  assert not consts
  return jaxpr, [core.ShapedArray(a.shape, a.dtype) for a in res_ref_avals]  # pytype: disable=attribute-error
