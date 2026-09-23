def remat_partial_eval(trace, *tracers, jaxpr, **params):
  assert not jaxpr.constvars
  if jaxpr.effects:
    raise NotImplementedError(
        'Effects not supported in partial-eval of `checkpoint`/`remat`.')
  policy = params['policy'] or nothing_saveable
  in_unknowns = [not t.is_known() for t in tracers]
  jaxpr_known, jaxpr_staged, out_unknowns, out_inst, num_res = \
      pe.partial_eval_jaxpr_custom(
          jaxpr, in_unknowns, [True] * len(in_unknowns), False, False, policy)

  # DCE jaxpr_staged, keeping only instantiated outputs which are unknown
  _, out_inst_unknown = partition_list(out_inst, out_unknowns)
  jaxpr_unknown, in_used_staged = pe.dce_jaxpr(jaxpr_staged, out_inst_unknown)
  used_res, in_used_staged = split_list(in_used_staged, [num_res])

  # DCE jaxpr_known, keeping all known outputs but discarding dce'd res
  out_used_known = [True] * (len(out_unknowns) - sum(out_unknowns)) + used_res
  jaxpr_known, in_used_known = pe.dce_jaxpr(jaxpr_known, out_used_known)
  num_res = sum(used_res)

  # compute known outputs and residuals (hoisted out of remat primitive)
  _, in_consts_ = unzip2(t.pval for t in tracers if t.pval.is_known())
  _, in_consts = partition_list(in_used_known, in_consts_)
  out_consts = core.eval_jaxpr(jaxpr_known, (), *in_consts)
  out_knowns, residuals = split_list(out_consts, [len(out_consts)-num_res])

  # set up unknown outputs with a recipe to call remat
  res_tracers = map(trace.new_instantiated_const, residuals)
  _, tracers_staged = partition_list(in_used_staged, tracers)
  in_jaxpr_tracers = res_tracers + map(trace.instantiate_const, tracers_staged)
  out_jaxpr_tracers = [pe.JaxprTracer(trace, pe.PartialVal.unknown(x.aval), None)
                       for x in jaxpr_unknown.outvars]
  new_params = dict(params, jaxpr=jaxpr_unknown, differentiated=True)
  recipe = pe.new_eqn_recipe(in_jaxpr_tracers, out_jaxpr_tracers, remat_p,
                             new_params, jaxpr_unknown.effects,
                             source_info_util.current())
  for t in out_jaxpr_tracers: t.recipe = recipe

  # zip together known and unknown outputs
  return merge_lists(out_unknowns, out_knowns, out_jaxpr_tracers)
