def transpose_jaxpr(jaxpr: core.Jaxpr, which_linear: List[bool]) -> core.Jaxpr:
  def trans(i, *args):
    # First we want to run the computation to read all the residual refs. We can
    # do that by using partial evaluation with all linear inputs unknown.
    res_jaxpr, tangent_jaxpr_, *_ = \
        _partial_eval_jaxpr_custom(jaxpr, [False, *which_linear],
                                   _save_everything)
    res_args = [x for x, lin in zip(args, which_linear) if not lin]
    res = core.eval_jaxpr(res_jaxpr, (), i, *res_args)

    # Now that we have residual values, we run the tangent jaxpr. It takes as
    # input the residuals, the loop index, and all the refs (at least, the ones
    # that are used in the body). Luckily, `tangent_jaxpr_` has all known and
    # unknown inputs!
    tangent_jaxpr, used = pe.dce_jaxpr(tangent_jaxpr_, [])
    used_res, (used_i,), used_ct = split_list(used, [len(res), 1])
    primals_args = [*(r for u, r in zip(used_res, res) if u)]
    if used_i:
      primals_args = [*primals_args, i]
    ct_args = [x for x, u in zip(args, used_ct) if u]
    ad.backward_pass(
        tangent_jaxpr, (), False, (), (*primals_args, *ct_args), ())
    return []
  jaxpr_trans, _, _ = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(trans), [v.aval for v in jaxpr.invars])
  return jaxpr_trans
