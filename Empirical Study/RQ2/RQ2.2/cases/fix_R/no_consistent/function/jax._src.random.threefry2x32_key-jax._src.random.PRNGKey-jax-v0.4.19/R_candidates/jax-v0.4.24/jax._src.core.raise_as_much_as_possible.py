def raise_as_much_as_possible(tracer) -> Tracer:
  # Find effective bottom of trace stack (highest dynamic Trace on the stack).
  trace_stack = thread_local_state.trace_state.trace_stack.stack
  idx = next(i for i, m in enumerate(trace_stack) if m is
             thread_local_state.trace_state.trace_stack.dynamic)

  # Only pay attention to effective part of trace stack.
  trace_stack = trace_stack[idx:]

  # Lift tracer into everything in the effective stack higher than its level
  for trace in trace_stack:
    trace = trace.with_cur_sublevel()
    if (not isinstance(tracer, Tracer) or tracer._trace.level < trace.level):
      tracer = trace.full_raise(tracer)

  return tracer
