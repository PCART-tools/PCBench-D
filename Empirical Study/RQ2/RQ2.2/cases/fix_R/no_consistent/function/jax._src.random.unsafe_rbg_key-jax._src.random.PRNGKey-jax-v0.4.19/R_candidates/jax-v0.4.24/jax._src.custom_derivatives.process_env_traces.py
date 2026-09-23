@partial(lu.transformation_with_aux, use_eq_store=True)
def process_env_traces(primitive, level: int, jvp_was_run: bool, *args):
  outs = yield args, {}
  todo = []
  while True:
    tracers = [x for x in outs if isinstance(x, core.Tracer)
               and (level is None or x._trace.level > level)]
    if tracers:
      ans = max(tracers, key=lambda x: x._trace.level)
    else:
      break
    trace = ans._trace.main.with_cur_sublevel()
    outs = map(trace.full_raise, outs)
    outs, cur_todo = primitive.post_process(trace, outs, jvp_was_run)
    todo.append(cur_todo)
  yield outs, tuple(todo)  # Ensure the aux output is immutable
