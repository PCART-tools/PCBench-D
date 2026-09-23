  def process_call(self, call_primitive, f, explicit_tracers, params):
    if f.in_type is None:
      f = lu.annotate(f, tuple((raise_to_shaped(t.aval), True)
                               for t in explicit_tracers))
    implicit_tracers = _extract_implicit_args(self, f.in_type, explicit_tracers)
    in_tracers = [*implicit_tracers, *explicit_tracers]
    # TODO(mattjj): check in_tracers are consistent with f.in_type annotation
    with core.new_sublevel():
      # TODO(lenamartens): Make call_primitive name -> API function name mapping.
      # (currently this will display eg. 'xla_call' instead of `jit`)
      dbg = debug_info_final(f, call_primitive.name)
      jaxpr, out_type, consts = trace_to_subjaxpr_dynamic2(f, self.main, debug_info=dbg)
    if params.get('inline', False):
      return core.eval_jaxpr(jaxpr, consts, *in_tracers,
                             propagate_source_info=False)
    source_info = source_info_util.current()
    out_tracers = []
    for aval, _ in out_type:
      if type(aval) is DShapedArray:
        shape = [[*consts, *in_tracers][d.val] if type(d) is InDBIdx else
                 out_tracers[d.val] if type(d) is OutDBIdx else
                 d for d in aval.shape]
        aval = aval.update(shape=tuple(get_referent(d) for d in shape))
      out_tracers.append(DynamicJaxprTracer(self, aval, source_info))
    invars = map(self.getvar, in_tracers)
    constvars = map(self.getvar, map(self.instantiate_const, consts))
    outvars = map(self.makevar, out_tracers)
    new_params = dict(params, call_jaxpr=convert_constvars_jaxpr(jaxpr))
    update_params = call_param_updaters.get(call_primitive)
    if update_params:
      new_params = update_params(new_params, [True] * len(explicit_tracers),
                                 len(consts) + len(implicit_tracers))
    eqn = new_jaxpr_eqn([*constvars, *invars], outvars, call_primitive,
                        new_params, new_params['call_jaxpr'].effects,
                        source_info)
    self.frame.add_eqn(eqn)
    return [t for t, (_, keep) in zip(out_tracers, out_type) if keep]
