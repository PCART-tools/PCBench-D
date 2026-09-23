def pjit_staging_rule(trace, *args, **params):
  if (params["inline"] and
      all(is_unspecified(i) for i in params["in_shardings"]) and
      all(is_unspecified(o) for o in params["out_shardings"])):
    jaxpr = params['jaxpr']
    return core.eval_jaxpr(jaxpr.jaxpr, jaxpr.consts, *args,
                           propagate_source_info=False)
  elif config.dynamic_shapes.value:
    source_info = source_info_util.current()
    out_tracers = []
    for aval in _out_type(params['jaxpr']):
      if type(aval) is core.DShapedArray:
        shape = [args[d.val] if type(d) is core.InDBIdx else
                 out_tracers[d.val] if type(d) is core.OutDBIdx else
                 d for d in aval.shape]
        aval = aval.update(shape=tuple(core.get_referent(d) for d in shape))
      out_tracers.append(pe.DynamicJaxprTracer(trace, aval, source_info))
    eqn = core.new_jaxpr_eqn(
      map(trace.getvar, args), map(trace.makevar, out_tracers), pjit_p, params,
      params['jaxpr'].effects, source_info)
    trace.frame.add_eqn(eqn)
    return out_tracers
  else:
    return trace.default_process_primitive(pjit_p, args, params)
