def trace_state_clean() -> bool:
  trace_state = thread_local_state.trace_state
  return (trace_state.substack == [Sublevel(0)] and
          trace_state.axis_env == [] and
          trace_state.trace_stack.stack == [MainTrace(0, EvalTrace)] and
          trace_state.trace_stack.dynamic == MainTrace(0, EvalTrace))
