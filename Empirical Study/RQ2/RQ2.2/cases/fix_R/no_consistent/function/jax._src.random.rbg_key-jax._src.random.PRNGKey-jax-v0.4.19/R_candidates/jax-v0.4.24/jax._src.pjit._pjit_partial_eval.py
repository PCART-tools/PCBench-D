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
  res_shardings = (UNSPECIFIED,) * num_residuals

  def keep_where(l, should_keep):
    return tuple(x for x, keep in zip(l, should_keep) if keep)

  # Compute which outputs are just forwarded inputs.
  num_out_primals = len(known_jaxpr.out_avals) - num_residuals
  in_fwd = pe._jaxpr_forwarding(known_jaxpr.jaxpr)

  # Only forward primal outputs when corresponding out_sharding is UNSPECIFIED.
  in_fwd_primal, in_fwd_res = split_list(in_fwd, [num_out_primals])
  in_fwd = [fwd if is_unspecified(os) else None for os, fwd in
            zip(keep_where(out_shardings, known_outs), in_fwd_primal)
            ] + in_fwd_res
  del in_fwd_primal, in_fwd_res

  # Compute which residuals are just primal outputs.
  out_vars, res_vars = split_list(known_jaxpr.jaxpr.outvars, [num_out_primals])
  idx_map = {id(v): i for i, v in enumerate(out_vars)}
  out_fwd = [None] * num_out_primals + [idx_map.get(id(v)) for v in res_vars]

  # Prune jaxpr outputs and out_shardings by removing forwards.
  keep = [f1 is None and f2 is None for f1, f2 in zip(in_fwd, out_fwd)]
  known_jaxpr = pe.prune_closed_jaxpr_outputs(known_jaxpr, keep)
  known_out_shardings = keep_where(out_shardings, known_outs) + res_shardings
  known_out_shardings = keep_where(known_out_shardings, keep)
  del keep, num_out_primals

  known_params = dict(
      jaxpr=known_jaxpr, in_shardings=keep_where(in_shardings, known_ins),
      out_shardings=known_out_shardings, resource_env=resource_env,
      donated_invars=keep_where(donated_invars, known_ins),
      name=name, keep_unused=keep_unused, inline=inline)
  assert len(known_params['out_shardings']) == len(known_params['jaxpr'].out_avals)

  # Bind known things to pjit_p.
  known_inputs = [pv.get_known() for pv in in_pvals if pv.is_known()]
  all_known_outs = pjit_p.bind(*known_inputs, **known_params)
  all_known_outs = subs_list2(in_fwd, out_fwd, known_inputs, all_known_outs,
                              all_known_outs)

  known_out_vals, residual_vals = \
      split_list(all_known_outs, [len(all_known_outs) - num_residuals])
  residual_tracers = map(trace.new_instantiated_const, residual_vals)

  # The convention of partial_eval_jaxpr_nounits is to place residual binders
  # at the front of the jaxpr produced, so we move them to the back since both
  # the jaxpr equation built below and the pjit transpose rule assume a
  # residual-inputs-last convention.
  unknown_jaxpr = pe.move_binders_to_back(
      unknown_jaxpr, [True] * num_residuals + [False] * sum(unknown_ins))
  # Prepare unknown tracers
  unknown_params = dict(
      jaxpr=unknown_jaxpr,
      in_shardings=(keep_where(in_shardings, unknown_ins) + res_shardings),
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
