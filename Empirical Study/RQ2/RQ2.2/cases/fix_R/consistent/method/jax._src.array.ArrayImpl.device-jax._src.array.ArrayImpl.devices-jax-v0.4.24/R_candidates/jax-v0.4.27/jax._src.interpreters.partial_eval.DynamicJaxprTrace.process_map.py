  def process_map(self, map_primitive, f, tracers, params):
    in_avals = [t.aval for t in tracers]
    axis_name, axis_size = params['axis_name'], params['axis_size']
    reduced_in_avals = [core.mapped_aval(axis_size, in_axis, a)
                        if in_axis is not None else a
                        for a, in_axis in zip(in_avals, params['in_axes'])]
    with core.extend_axis_env(axis_name, params["global_axis_size"], None):  # type: ignore
      with core.new_sublevel():
        jaxpr, reduced_out_avals, consts, () = trace_to_subjaxpr_dynamic(
            f, self.main, reduced_in_avals,
            debug_info=debug_info_final(f, map_primitive.name))
      ordered_effects = effects.ordered_effects.filter_in(jaxpr.effects)
      if ordered_effects:
        raise ValueError("Ordered effects not supported for "
                         f"map primitives: {ordered_effects}")
      out_axes = params['out_axes_thunk']()
      out_avals = [core.unmapped_aval(axis_size, axis_name, out_axis, a)
                  if out_axis is not None else a
                  for a, out_axis in zip(reduced_out_avals, out_axes)]
      source_info = source_info_util.current()
      out_tracers = [DynamicJaxprTracer(self, a, source_info) for a in out_avals]
      invars = map(self.getvar, tracers)
      constvars = map(self.getvar, map(self.instantiate_const, consts))
      outvars = map(self.makevar, out_tracers)
      new_in_axes = (None,) * len(consts) + params['in_axes']
      new_params = dict(params, in_axes=new_in_axes, out_axes=out_axes,
                        call_jaxpr=convert_constvars_jaxpr(jaxpr))
      del new_params['out_axes_thunk']
      update_params = call_param_updaters.get(map_primitive)
      if update_params:
        new_params = update_params(new_params, [True] * len(tracers), len(consts))
      effs = core.filter_named_axis_effects(jaxpr.effects, {axis_name})
      eqn = new_jaxpr_eqn([*constvars, *invars], outvars, map_primitive,
                          new_params, effs, source_info)
      self.frame.add_eqn(eqn)
    return out_tracers
