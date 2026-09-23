def reset_trace_state() -> bool:
  """Resets the global trace state and returns True if it was already clean."""
  if not trace_state_clean():
    thread_local_state.trace_state.__init__()  # type: ignore
    return False
  else:
    return True
