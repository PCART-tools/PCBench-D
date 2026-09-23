def closed_call_partial_eval_custom_rule(
    jaxpr_param_name: str, params_updater: ParamsUpdater,
    saveable: Callable[..., bool], unks_in: list[bool], inst_in: list[bool],
    eqn: JaxprEqn, *, res_aval: ResAvalUpdater = _default_res_aval_updater,
  ) -> tuple[JaxprEqn, JaxprEqn, Sequence[bool], Sequence[bool], list[Var]]:
  # TODO(sharadmv,mattjj): dedup this rule with call_partial_eval_custom_rule.
  closed_jaxpr = eqn.params[jaxpr_param_name]
  jaxpr_known_, jaxpr_staged_, unks_out, inst_out, num_res_out, num_res_ref = \
      partial_eval_jaxpr_stateful(closed_jaxpr.jaxpr, unks_in, inst_in,
                                  False, False, saveable)
  num_res = num_res_ref + num_res_out
  # Forming these fresh ClosedJaxprs defeats caching, but caller handles caching
  jaxpr_known = core.ClosedJaxpr(jaxpr_known_, closed_jaxpr.consts)
  jaxpr_staged = core.ClosedJaxpr(jaxpr_staged_, closed_jaxpr.consts)
  ins_known, _ = partition_list(unks_in, eqn.invars)
  out_binders_known, _ = partition_list(unks_out, eqn.outvars)
  _, ins_staged = partition_list(inst_in, eqn.invars)
  _, out_binders_staged = partition_list(inst_out, eqn.outvars)
  newvar = core.gensym([jaxpr_known.jaxpr, jaxpr_staged.jaxpr])
  params_known = {**eqn.params, jaxpr_param_name: jaxpr_known}
  params_staged = {**eqn.params, jaxpr_param_name: jaxpr_staged}
  params_known, params_staged = params_updater(
      unks_in, inst_in, map(op.not_, unks_out), inst_out, num_res, params_known,
      params_staged)
  residuals, ref_residuals = split_list(
      [newvar(res_aval(params_known, v)) for v
       in jaxpr_staged.in_avals[:num_res]], [num_res_out])
  eqn_known = new_jaxpr_eqn([*ins_known, *ref_residuals],
                            [*out_binders_known, *residuals],
                            eqn.primitive, params_known, jaxpr_known.effects,
                            eqn.source_info)
  eqn_staged = new_jaxpr_eqn([*residuals, *ref_residuals, *ins_staged],
                             out_binders_staged,
                             eqn.primitive, params_staged, jaxpr_staged.effects,
                             eqn.source_info)
  assert len(eqn_staged.invars) == len(jaxpr_staged.in_avals)
  assert len(ins_known) + len(ref_residuals) == len(jaxpr_known.jaxpr.invars)
  assert len(ins_staged) + len(ref_residuals) + len(residuals) == len(jaxpr_staged.jaxpr.invars)
  assert len(out_binders_known) + len(residuals) == len(jaxpr_known.jaxpr.outvars)
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is Var and not inst]
  new_vars = [*new_inst, *residuals, *ref_residuals]
  return eqn_known, eqn_staged, unks_out, inst_out, new_vars
