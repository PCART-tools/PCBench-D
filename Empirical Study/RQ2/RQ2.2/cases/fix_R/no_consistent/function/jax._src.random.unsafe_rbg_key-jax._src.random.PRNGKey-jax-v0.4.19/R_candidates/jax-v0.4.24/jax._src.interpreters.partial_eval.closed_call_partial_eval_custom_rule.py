def closed_call_partial_eval_custom_rule(
    jaxpr_param_name: str, params_updater: ParamsUpdater2,
    saveable: Callable[..., RematCases_], unks_in: list[bool], inst_in: list[bool],
    eqn: JaxprEqn, *, res_aval: ResAvalUpdater = _default_res_aval_updater,
  ) -> tuple[JaxprEqn, JaxprEqn, Sequence[bool], Sequence[bool], list[Var]]:
  # TODO(sharadmv,mattjj): dedup this rule with call_partial_eval_custom_rule.
  dropvars = tuple(isinstance(v, DropVar) for v in eqn.outvars)
  jaxpr_known, jaxpr_staged, unks_out, inst_out, num_res_ref, num_res_val, out_fwd = \
      _closed_jaxpr_partial_eval_custom_cached(
          eqn.params[jaxpr_param_name], (*unks_in,), (*inst_in,), dropvars, saveable)
  num_res = num_res_ref + num_res_val
  out_binders_known, _ = partition_list(unks_out, eqn.outvars)
  ins_known, _ = partition_list(unks_in, eqn.invars)
  _, ins_staged = partition_list(inst_in, eqn.invars)
  _, out_binders_staged = partition_list(inst_out, eqn.outvars)
  newvar = core.gensym([jaxpr_known.jaxpr, jaxpr_staged.jaxpr])
  params_known = {**eqn.params, jaxpr_param_name: jaxpr_known}
  params_staged = {**eqn.params, jaxpr_param_name: jaxpr_staged}
  params_known, params_staged = params_updater(
      unks_in, inst_in, map(op.not_, unks_out), inst_out,
      sum(f is None for f in out_fwd), num_res, params_known, params_staged)
  res_val_binders, res_ref_binders = split_list(
      [newvar(res_aval(params_known, v))
       for v in jaxpr_staged.in_avals[:num_res]], [num_res_val])
  res_val_binders = [v for v, f in zip(res_val_binders, out_fwd) if f is None]
  res_val_vars = subs_list(out_fwd, out_binders_known, res_val_binders)
  eqn_known = new_jaxpr_eqn([*ins_known, *res_ref_binders],
                            [*out_binders_known, *res_val_binders],
                            eqn.primitive, params_known, jaxpr_known.effects,
                            eqn.source_info)
  eqn_staged = new_jaxpr_eqn([*res_val_vars, *res_ref_binders, *ins_staged],
                             out_binders_staged,
                             eqn.primitive, params_staged, jaxpr_staged.effects,
                             eqn.source_info)
  assert len(eqn_staged.invars) == len(jaxpr_staged.in_avals)
  assert len(ins_known) + len(res_ref_binders) == len(jaxpr_known.jaxpr.invars)
  assert len(ins_staged) + len(res_ref_binders) + len(res_val_vars) == len(jaxpr_staged.jaxpr.invars)
  assert len(out_binders_known) + len(res_val_binders) == len(jaxpr_known.jaxpr.outvars)
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is Var and not inst]
  new_vars = [*new_inst, *res_val_vars, *res_ref_binders]
  return eqn_known, eqn_staged, unks_out, inst_out, new_vars
