def _join_cond_outputs(jaxprs, all_res_avals, res_aval_indices_per_jaxpr,
                       num_non_res_outputs):
  def augment_jaxpr(jaxpr, res_indices):
    @lu.wrap_init
    def f_aug(*args):
      outs_and_residuals = core.jaxpr_as_fun(jaxpr)(*args)
      outs, residuals = split_list(outs_and_residuals, [num_non_res_outputs])
      aug_residuals = map(ad_util.zeros_like_aval, all_res_avals)
      aug_residuals = util.subvals(aug_residuals, zip(res_indices, residuals))
      return outs + list(aug_residuals)

    return _make_closed_jaxpr(f_aug, jaxpr.in_avals)

  return tuple(map(augment_jaxpr, jaxprs, res_aval_indices_per_jaxpr))
