def _pmap_dce_rule(used_outputs, eqn):
  # just like pe.dce_jaxpr_call_rule, except handles in_axes / out_axes
  with maybe_extend_axis_env(eqn.params['axis_name'],
                             eqn.params['global_axis_size'], None):
    new_jaxpr, used_inputs = pe.dce_jaxpr(eqn.params['call_jaxpr'], used_outputs)
  _, donated_invars = partition_list(used_inputs, eqn.params['donated_invars'])
  _, in_axes = partition_list(used_inputs, eqn.params['in_axes'])
  _, out_axes = partition_list(used_outputs, eqn.params['out_axes'])
  new_params = dict(eqn.params, call_jaxpr=new_jaxpr,
                    donated_invars=tuple(donated_invars),
                    in_axes=tuple(in_axes), out_axes=tuple(out_axes))
  if not any(used_inputs) and not any(used_outputs) and not new_jaxpr.effects:
    return used_inputs, None
  else:
    new_eqn = pe.new_jaxpr_eqn(
        [v for v, used in zip(eqn.invars, used_inputs) if used],
        [v for v, used in zip(eqn.outvars, used_outputs) if used],
        eqn.primitive, new_params, new_jaxpr.effects, eqn.source_info)
    return used_inputs, new_eqn
