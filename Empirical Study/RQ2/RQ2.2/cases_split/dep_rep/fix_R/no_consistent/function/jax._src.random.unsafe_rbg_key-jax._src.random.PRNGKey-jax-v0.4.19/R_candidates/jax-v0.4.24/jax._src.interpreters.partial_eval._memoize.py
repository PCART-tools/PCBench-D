def _memoize(fn):
  cells = {}
  saved_state = core.thread_local_state.trace_state.copy()
  sentinel = object()
  def memoized(*args):
    out = cells.get(args, sentinel)
    if out is sentinel:
      prev_state = core.thread_local_state.trace_state
      core.thread_local_state.trace_state = saved_state
      try:
        out = cells[args] = fn(*args)
      finally:
        core.thread_local_state.trace_state = prev_state
    return out
  return memoized
