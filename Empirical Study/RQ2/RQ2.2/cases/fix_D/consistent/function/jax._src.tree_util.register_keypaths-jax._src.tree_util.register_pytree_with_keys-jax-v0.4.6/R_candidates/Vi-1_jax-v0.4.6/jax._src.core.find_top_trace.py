def find_top_trace(xs) -> Trace:
  top_tracer = max((x for x in xs if isinstance(x, Tracer)),
                    default=None, key=attrgetter('_trace.level'))
  if top_tracer is not None:
    top_tracer._assert_live()
    top_main = top_tracer._trace.main
  else:
    top_main = None  # type: ignore
  dynamic = thread_local_state.trace_state.trace_stack.dynamic
  top_main = (dynamic if top_main is None or dynamic.level > top_main.level
              else top_main)
  return top_main.with_cur_sublevel()  # type: ignore
