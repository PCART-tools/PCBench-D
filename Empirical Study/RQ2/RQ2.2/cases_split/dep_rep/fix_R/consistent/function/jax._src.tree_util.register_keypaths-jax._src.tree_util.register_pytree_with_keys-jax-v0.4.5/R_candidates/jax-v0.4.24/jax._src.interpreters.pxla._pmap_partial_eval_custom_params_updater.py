def _pmap_partial_eval_custom_params_updater(
    unks_in, inst_in, kept_outs_known, kept_outs_staged, num_res, params_known,
    params_staged):
  # prune inputs to jaxpr_known according to unks_in
  donated_invars_known, _ = partition_list(unks_in, params_known['donated_invars'])
  in_axes_known, _ = partition_list(unks_in, params_known['in_axes'])
  _, out_axes_known = partition_list(kept_outs_known, params_known['out_axes'])
  out_axes_known = out_axes_known + [0] * num_res
  new_params_known = dict(params_known, in_axes=tuple(in_axes_known),
                          out_axes=tuple(out_axes_known),
                          donated_invars=tuple(donated_invars_known))

  # added num_res new inputs to jaxpr_staged, pruning according to inst_in
  _, donated_invars_staged = partition_list(inst_in, params_staged['donated_invars'])
  donated_invars_staged = [False] * num_res + donated_invars_staged
  _, in_axes_staged = partition_list(inst_in, params_staged['in_axes'])
  in_axes_staged = [0] * num_res + in_axes_staged
  _, out_axes_staged = partition_list(kept_outs_staged, params_staged['out_axes'])
  new_params_staged = dict(params_staged, in_axes=tuple(in_axes_staged),
                           out_axes=tuple(out_axes_staged),
                           donated_invars=tuple(donated_invars_staged))
  return new_params_known, new_params_staged
