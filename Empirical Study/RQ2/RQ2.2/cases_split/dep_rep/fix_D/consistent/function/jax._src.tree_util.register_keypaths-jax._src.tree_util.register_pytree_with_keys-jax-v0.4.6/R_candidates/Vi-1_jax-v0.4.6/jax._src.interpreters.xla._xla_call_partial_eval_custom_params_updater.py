def _xla_call_partial_eval_custom_params_updater(
    unks_in: Sequence[bool], inst_in: Sequence[bool],
    kept_outs_known: Sequence[bool], kept_outs_staged: Sequence[bool],
    num_res: int, params_known: dict, params_staged: dict
  ) -> Tuple[dict, dict]:
  # pruned inputs to jaxpr_known according to unks_in, so prune donated_invars
  donated_known, _ = partition_list(unks_in, params_known['donated_invars'])
  new_params_known = dict(params_known, donated_invars=tuple(donated_known))
  # added num_res new inputs to jaxpr_staged, so extend donated_invars
  _, donated_staged_ = partition_list(inst_in, params_staged['donated_invars'])
  donated_staged = [False] * num_res + donated_staged_
  new_params_staged = dict(params_staged, donated_invars=tuple(donated_staged))
  return new_params_known, new_params_staged
