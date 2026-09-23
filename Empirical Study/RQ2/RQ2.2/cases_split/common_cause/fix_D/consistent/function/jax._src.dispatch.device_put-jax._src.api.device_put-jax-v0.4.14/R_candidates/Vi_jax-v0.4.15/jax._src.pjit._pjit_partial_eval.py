def _pjit_partial_eval(trace, *in_tracers,
                       jaxpr, in_shardings, out_shardings,
                       resource_env, donated_invars, name, keep_unused, inline):
  in_pvals = [t.pval for t in in_tracers]

  known_ins = tuple(pv.is_known() for pv in in_pvals)
  unknown_ins = tuple(not k for k in known_ins)
  known_jaxpr, unknown_jaxpr, unknown_outs, res_avals = pe.partial_eval_jaxpr_nounits(
      jaxpr, unknown_ins, instantiate=False)
  unknown_outs = tuple(unknown_outs)
  known_outs = tuple(not uk for uk in unknown_outs)
  num_residuals = len(res_avals)

  def keep_where(l, should_keep):
    return tuple(x for x, keep in unsafe_zip(l, should_keep) if keep)

  residual_shardings = (UNSPECIFIED,) * num_residuals
  # Compute the known outputs
  known_params = dict(
      jaxpr=known_jaxpr,
      in_shardings=keep_where(in_shardings, known_ins),
      out_shardings=(
          keep_where(out_shardings, known_outs) + residual_shardings),
      resource_env=resource_env,
      donated_invars=keep_where(donated_invars, known_ins),
      name=name,
      keep_unused=keep_unused,
      inline=inline)

  fwds_known = pe._jaxpr_forwarding(known_params['jaxpr'].jaxpr)

  # Only forward the outvars where the out_sharding is UNSPECIFIED.
  known_user_out_shardings = keep_where(known_params['out_shardings'], known_outs)
  fwds_known_user = [
      fwd if is_unspecified(os) else None
      for os, fwd in zip(known_user_out_shardings,
                              fwds_known[:len(known_user_out_shardings)])]
  fwds_known = fwds_known_user + fwds_known[len(known_user_out_shardings):]
  del fwds_known_user

  # Remove forwarded outvars and out_shardings
  known_params['jaxpr'] = _known_jaxpr_fwd(known_params['jaxpr'], tuple(fwds_known))
  known_out_shardings = tuple(
      s for s, i in zip(known_params['out_shardings'], fwds_known) if i is None)
  known_params['out_shardings'] = known_out_shardings
  del known_out_shardings

  assert len(known_params['out_shardings']) == len(known_params['jaxpr'].out_avals)

  # Bind known things to pjit_p.
  known_inputs = [pv.get_known() for pv in in_pvals if pv.is_known()]
  all_known_outs = pjit_p.bind(*known_inputs, **known_params)

  known_outs_iter = iter(all_known_outs)
  all_known_outs = [next(known_outs_iter)
                    if fwd_idx is None else known_inputs[fwd_idx]
                    for fwd_idx in fwds_known]
  assert next(known_outs_iter, None) is None
  del known_outs_iter, known_inputs

  if num_residuals:
    known_out_vals, residual_vals = \
        split_list(all_known_outs, [len(all_known_outs) - num_residuals])
  else:
    known_out_vals, residual_vals = all_known_outs, ()
  residual_tracers = [trace.new_instantiated_const(residual) for residual in residual_vals]

  # The convention of partial_eval_jaxpr_nounits is to place residual binders
  # at the front of the jaxpr produced, so we move them to the back since both
  # the jaxpr equation built below and the pjit transpose rule assume a
  # residual-inputs-last convention.
  unknown_jaxpr = pe.move_binders_to_back(
      unknown_jaxpr, [True] * num_residuals + [False] * sum(unknown_ins))
  # Prepare unknown tracers
  unknown_params = dict(
      jaxpr=unknown_jaxpr,
      in_shardings=(keep_where(in_shardings, unknown_ins) + residual_shardings),
      out_shardings=keep_where(out_shardings, unknown_outs),
      resource_env=resource_env,
      donated_invars=(keep_where(donated_invars, unknown_ins) +
                      (False,) * num_residuals),
      name=name,
      keep_unused=keep_unused,
      inline=inline)
  unknown_tracers_in = [t for t in in_tracers if not t.pval.is_known()]
  unknown_out_avals = unknown_jaxpr.out_avals
  unknown_tracers_out = [
      pe.JaxprTracer(trace, pe.PartialVal.unknown(aval), None)
      for aval in unknown_out_avals
  ]
  eqn = pe.new_eqn_recipe((*unknown_tracers_in, *residual_tracers),
                          unknown_tracers_out,
                          pjit_p,
                          unknown_params,
                          unknown_jaxpr.effects,
                          source_info_util.current())
  for t in unknown_tracers_out: t.recipe = eqn
  return merge_lists(unknown_outs, known_out_vals, unknown_tracers_out)
