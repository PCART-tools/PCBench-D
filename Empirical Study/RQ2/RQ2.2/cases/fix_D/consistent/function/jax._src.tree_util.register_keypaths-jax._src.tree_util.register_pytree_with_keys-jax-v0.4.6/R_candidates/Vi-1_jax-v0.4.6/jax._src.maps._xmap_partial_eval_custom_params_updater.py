def _xmap_partial_eval_custom_params_updater(
    unks_in: Sequence[bool], inst_in: Sequence[bool],
    kept_outs_known: Sequence[bool], kept_outs_staged: Sequence[bool],
    num_res: int, params_known: dict, params_staged: dict
  ) -> Tuple[dict, dict]:
  assert params_known['spmd_in_axes'] is None is params_known['spmd_out_axes']
  assert params_staged['spmd_in_axes'] is None is params_staged['spmd_out_axes']

  # prune inputs to jaxpr_known according to unks_in
  donated_invars_known, _ = pe.partition_list(unks_in, params_known['donated_invars'])
  in_axes_known, _ = pe.partition_list(unks_in, params_known['in_axes'])
  if num_res == 0:
    residual_axes = []
  else:
    residual_axes = [
      AxisNamePos(zip(sort_named_shape, range(len(sort_named_shape))),
                  user_repr=f'<internal: {sort_named_shape}>')
      for named_shape in (v.aval.named_shape for v in params_known['call_jaxpr'].outvars[:-num_res])
      # We sort here to make the iteration order deterministic
      for sort_named_shape in [sorted(named_shape, key=str)]
    ]
  _, out_axes_known = pe.partition_list(kept_outs_known, params_known['out_axes'])
  new_params_known = dict(params_known,
                          in_axes=tuple(in_axes_known),
                          out_axes=(*out_axes_known, *residual_axes),
                          donated_invars=tuple(donated_invars_known))
  assert len(new_params_known['in_axes']) == len(params_known['call_jaxpr'].invars)
  assert len(new_params_known['out_axes']) == len(params_known['call_jaxpr'].outvars)

  # added num_res new inputs to jaxpr_staged, and pruning according to inst_in
  _, donated_invars_staged = pe.partition_list(inst_in, params_staged['donated_invars'])
  donated_invars_staged = [False] * num_res + donated_invars_staged
  _, in_axes_staged = pe.partition_list(inst_in, params_staged['in_axes'])
  in_axes_staged = [*residual_axes, *in_axes_staged]
  _, out_axes_staged = pe.partition_list(kept_outs_staged, params_staged['out_axes'])
  new_params_staged = dict(params_staged, in_axes=tuple(in_axes_staged),
                           out_axes=tuple(out_axes_staged),
                           donated_invars=tuple(donated_invars_staged))
  assert len(new_params_staged['in_axes']) == len(params_staged['call_jaxpr'].invars)
  assert len(new_params_staged['out_axes']) == len(params_staged['call_jaxpr'].outvars)
  return new_params_known, new_params_staged
