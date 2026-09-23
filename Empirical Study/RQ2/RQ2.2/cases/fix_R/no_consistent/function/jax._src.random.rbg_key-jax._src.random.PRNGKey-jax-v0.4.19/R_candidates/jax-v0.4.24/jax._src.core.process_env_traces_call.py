@lu.transformation_with_aux
def process_env_traces_call(primitive: CallPrimitive, level: int,
                            params_tuple: tuple, *args):
  outs = yield args, {}
  params = dict(params_tuple)
  todo = []
  while True:
    tracers = [x for x in outs if isinstance(x, Tracer) and x._trace.level > level]
    if not tracers:
      break
    ans = max(tracers, key=operator.attrgetter('_trace.level'))
    trace = ans._trace.main.with_cur_sublevel()
    outs = map(trace.full_raise, outs)
    outs, cur_todo = trace.post_process_call(primitive, outs, params)
    todo.append(cur_todo)
  yield outs, tuple(todo)  # Ensure the aux output is immutable
