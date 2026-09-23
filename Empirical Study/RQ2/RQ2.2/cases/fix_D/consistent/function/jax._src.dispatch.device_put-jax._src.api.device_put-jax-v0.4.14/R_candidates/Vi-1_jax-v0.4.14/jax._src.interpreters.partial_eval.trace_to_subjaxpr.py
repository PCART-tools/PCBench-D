@lu.transformation
def trace_to_subjaxpr(main: core.MainTrace, instantiate: bool | Sequence[bool],
                      pvals: Sequence[PartialVal]):
  assert all([isinstance(pv, PartialVal) for pv in pvals]), pvals
  trace = main.with_cur_sublevel()
  in_tracers = map(trace.new_arg, pvals)
  ans = yield in_tracers, {}
  assert isinstance(ans, (list, tuple)), (
      f"Got unexpected return type when tracing function to jaxpr: {ans}")
  assert all(isinstance(x, core.Tracer) or core.valid_jaxtype(x) for x in ans), (
      f"Got unexpected return type when tracing function to jaxpr: {ans}")
  instantiate = [instantiate] * len(ans) if isinstance(instantiate, bool) else instantiate
  out_tracers = map(trace.full_raise, map(core.full_lower, ans))
  out_tracers = map(partial(instantiate_const_at, trace), instantiate, out_tracers)
  jaxpr, consts, env = tracers_to_jaxpr(in_tracers, out_tracers)
  out_pvals = [t.pval for t in out_tracers]
  del trace, in_tracers, out_tracers
  yield jaxpr, (out_pvals, consts, env)
