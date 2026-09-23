def _dynamic_jaxpr_process_xmap(self, primitive, f, tracers, params):
  assert primitive is xmap_p
  in_avals = [t.aval for t in tracers]
  global_axis_sizes = params['global_axis_sizes']
  mapped_in_avals = [_delete_aval_axes(a, a_in_axes, global_axis_sizes)
                     for a, a_in_axes in zip(in_avals, params['in_axes'])]
  with core.extend_axis_env_nd(global_axis_sizes.items()):
    with core.new_sublevel():
      jaxpr, mapped_out_avals, consts = trace_to_subjaxpr_dynamic(
          f, self.main, mapped_in_avals)
  out_axes = params['out_axes_thunk']()
  if params['spmd_out_axes_thunk'] is not None:
    spmd_out_axes = params['spmd_out_axes_thunk']()
  else:
    spmd_out_axes = None
  axis_resource_count = _get_axis_resource_count(
      params['axis_resources'], params['resource_env'])
  local_axis_sizes = {
      axis: axis_resource_count[axis].to_local(global_size)
      for axis, global_size in global_axis_sizes.items()
  }
  out_avals = [_insert_aval_axes(a, a_out_axes, local_axis_sizes)
               for a, a_out_axes in zip(mapped_out_avals, out_axes)]
  _check_out_avals_vs_out_axes(out_avals, out_axes, params['global_axis_sizes'])
  source_info = source_info_util.current()
  out_tracers = [DynamicJaxprTracer(self, a, source_info) for a in out_avals]
  invars = map(self.getvar, tracers)
  constvars = map(self.getvar, map(self.instantiate_const, consts))
  outvars = map(self.makevar, out_tracers)
  new_in_axes = (AxisNamePos(user_repr='{}'),) * len(consts) + params['in_axes']
  if params['spmd_in_axes'] is None:
    new_spmd_in_axes = None
  else:
    new_spmd_in_axes = (None,) * len(consts) + params['spmd_in_axes']
  new_donated_invars = (False,) * len(consts) + params['donated_invars']
  with core.extend_axis_env_nd(global_axis_sizes.items()):
    call_jaxpr = convert_constvars_jaxpr(jaxpr)
  new_params = dict(params, in_axes=new_in_axes, out_axes=out_axes,
                    donated_invars=new_donated_invars,
                    spmd_in_axes=new_spmd_in_axes,
                    spmd_out_axes=spmd_out_axes,
                    call_jaxpr=call_jaxpr)
  del new_params['out_axes_thunk']
  del new_params['spmd_out_axes_thunk']
  eqn = new_jaxpr_eqn([*constvars, *invars], outvars, primitive,
                      new_params, call_jaxpr.effects, source_info)
  self.frame.add_eqn(eqn)
  return out_tracers
