def cur_sublevel() -> Sublevel:
  return thread_local_state.trace_state.substack[-1]
