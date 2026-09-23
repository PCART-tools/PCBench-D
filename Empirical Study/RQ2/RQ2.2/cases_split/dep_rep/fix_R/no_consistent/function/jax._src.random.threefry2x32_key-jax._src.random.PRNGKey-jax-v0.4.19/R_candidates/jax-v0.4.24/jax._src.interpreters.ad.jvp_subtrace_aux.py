@lu.transformation_with_aux
def jvp_subtrace_aux(main, primals, tangents):
  trace = JVPTrace(main, core.cur_sublevel())
  for x in list(primals) + list(tangents):
    if isinstance(x, Tracer):
      assert x._trace.level < trace.level
  ans, aux = yield map(partial(JVPTracer, trace), primals, tangents), {}
  ans_tracers = map(trace.full_raise, ans)
  out_primals, out_tangents = unzip2((t.primal, t.tangent) for t in ans_tracers)
  aux_primals = [core.full_lower(x.primal)
                 if isinstance(x, JVPTracer) and x._trace.level == trace.level
                 else x for x in aux]
  yield (out_primals, out_tangents), aux_primals
