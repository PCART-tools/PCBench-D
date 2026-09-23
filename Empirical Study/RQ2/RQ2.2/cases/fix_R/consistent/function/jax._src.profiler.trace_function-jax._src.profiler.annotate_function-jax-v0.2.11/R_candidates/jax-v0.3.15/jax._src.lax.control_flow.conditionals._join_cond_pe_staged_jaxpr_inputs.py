def _join_cond_pe_staged_jaxpr_inputs(jaxprs, all_res_avals,
                                      res_aval_indices_per_jaxpr):
  newvar = core.gensym([j.jaxpr for j in jaxprs], suffix='_')
  all_res_vars = _map(newvar, all_res_avals)

  def augment_jaxpr(jaxpr, res_indices):
    num_res = len(res_indices)
    res_vars = jaxpr.jaxpr.invars[:num_res]
    non_res_vars = jaxpr.jaxpr.invars[num_res:]

    aug_res_vars = list(util.subvals(all_res_vars, zip(res_indices, res_vars)))
    aug_invars = aug_res_vars + non_res_vars
    jaxpr_aug = core.Jaxpr(jaxpr.jaxpr.constvars, aug_invars,
                           jaxpr.jaxpr.outvars, jaxpr.jaxpr.eqns,
                           jaxpr.jaxpr.effects)
    jaxpr_aug = core.ClosedJaxpr(jaxpr_aug, jaxpr.consts)
    return jaxpr_aug

  return tuple(_map(augment_jaxpr, jaxprs, res_aval_indices_per_jaxpr))
