@lu.transformation_with_aux
def checkify_subtrace(main, msgs, err, code, payload, *args):
  setnewattr(main, 'error', Error(err, code, dict(msgs), payload))
  trace = main.with_cur_sublevel()
  in_tracers = [CheckifyTracer(trace, x) for x in args]
  out = yield in_tracers, {}
  out_tracers = map(trace.full_raise, out)
  out_vals = [t.val for t in out_tracers]
  err, code, payload, msgs = main.error.err, main.error.code, main.error.payload, main.error.msgs
  del main.error
  yield (err, code, payload, *out_vals), msgs
