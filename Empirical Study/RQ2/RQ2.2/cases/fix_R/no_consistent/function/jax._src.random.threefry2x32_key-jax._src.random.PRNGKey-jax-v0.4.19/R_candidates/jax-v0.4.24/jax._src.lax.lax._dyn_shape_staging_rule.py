def _dyn_shape_staging_rule(trace, prim, out_aval, *args, **params):
  source_info = source_info_util.current()
  out_tracer = pe.DynamicJaxprTracer(trace, out_aval, source_info)
  eqn = pe.new_jaxpr_eqn([trace.getvar(x) for x in args],
                         [trace.makevar(out_tracer)],
                         prim, params, core.no_effects, source_info)
  trace.frame.add_eqn(eqn)
  return out_tracer
