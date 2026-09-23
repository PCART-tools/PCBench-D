def _transpose_jaxpr(jaxpr: core.Jaxpr, which_linear: Sequence[bool]
                    ) -> tuple[core.Jaxpr, Any]:
  def trans(*args):
    # First we want to run the computation to read all the residual refs. We can
    # do that by using partial evaluation with all linear inputs unknown.
    res_jaxpr_, tangent_jaxpr_, *_, num_res_out, num_res_ref = \
        pe.partial_eval_jaxpr_stateful(jaxpr, which_linear, in_inst=which_linear,
                                       ensure_out_inst=[],
                                       ensure_out_unknowns=[],
                                       saveable=_save_everything)

    num_unknown = sum(which_linear)
    num_known = len(jaxpr.invars) - num_unknown
    res_args, _ = partition_list(which_linear, args)
    res_jaxpr_avals = [v.aval for v in res_jaxpr_.invars]
    _, res_avals = split_list(res_jaxpr_avals, [num_known])
    res_avals = [a.inner_aval for a in res_avals]  # pytype: disable=attribute-error
    all_avals = [*res_avals, *[v.aval for v in res_jaxpr_.outvars]]
    empty_res = map(ad.zeros_like_aval, all_avals)
    res_jaxpr, _ = _convert_outputs_to_writes(res_jaxpr_)
    res = run_state_p.bind(*res_args, *empty_res, jaxpr=res_jaxpr,
                           which_linear=(False,) * (len(res_args) + len(empty_res)))
    res = res[len(res_args):]
    ref_res_, nonref_res_ = split_list(res, [num_res_ref])

    # Now that we have residual values, we run the tangent jaxpr. It takes as
    # input the residuals, the loop index, and all the refs (at least, the ones
    # that are used in the body). Luckily, `tangent_jaxpr_` has all known and
    # unknown inputs!
    tangent_jaxpr, used_inputs = pe.dce_jaxpr(tangent_jaxpr_, [])
    used_res, used_cts = split_list(used_inputs, [len(res)])
    used_nonref_res, used_ref_res = split_list(used_res, [num_res_out])
    _, nonref_res = partition_list(used_nonref_res, nonref_res_)
    _, ref_res = partition_list(used_ref_res, ref_res_)
    primals_args = [*nonref_res, *ref_res]
    _, tangent_args = partition_list(which_linear, args)
    _, ct_args = partition_list(used_cts, tangent_args)
    ad.backward_pass(
        tangent_jaxpr, (), False, (), (*primals_args, *ct_args), ())
    return []
  jaxpr_trans, _, consts, () = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(trans), [v.aval for v in jaxpr.invars])
  return jaxpr_trans, consts
