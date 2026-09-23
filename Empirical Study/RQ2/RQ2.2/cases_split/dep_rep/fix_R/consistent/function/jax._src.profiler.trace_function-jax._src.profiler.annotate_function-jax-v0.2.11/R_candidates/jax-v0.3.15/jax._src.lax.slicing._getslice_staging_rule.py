def _getslice_staging_rule(trace, x, lo, hi):
  size = lax.make_bint(lax.clamp(0, hi - lo, x.shape[0]), x.shape[0])
  aval = core.DShapedArray((size,), x.dtype, x.weak_type)
  source_info = source_info_util.current()
  out_tracer = pe.DynamicJaxprTracer(trace, aval, source_info)
  invars = map(trace.getvar, [x, lo, hi])
  eqn = pe.new_jaxpr_eqn(invars, [trace.makevar(out_tracer)],
                         getslice_p, {}, source_info)
  trace.frame.eqns.append(eqn)
  return out_tracer
