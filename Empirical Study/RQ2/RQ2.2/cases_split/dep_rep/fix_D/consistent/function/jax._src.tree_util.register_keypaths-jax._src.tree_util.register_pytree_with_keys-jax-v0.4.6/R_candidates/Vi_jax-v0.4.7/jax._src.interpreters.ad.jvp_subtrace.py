@lu.transformation
def jvp_subtrace(main, primals, tangents):
  trace = JVPTrace(main, core.cur_sublevel())
  for x in list(primals) + list(tangents):
    if isinstance(x, Tracer):
      if x._trace.level >= trace.level:
        raise core.escaped_tracer_error(
            x, f"Tracer from a higher level: {x} in trace {trace}")
      assert x._trace.level < trace.level
  in_tracers = [JVPTracer(trace, x, t) if type(t) is not Zero else x
                for x, t in zip(primals, tangents)]
  ans = yield in_tracers, {}
  out_tracers = map(trace.full_raise, ans)
  yield unzip2([(out_tracer.primal, out_tracer.tangent)
                for out_tracer in out_tracers])
