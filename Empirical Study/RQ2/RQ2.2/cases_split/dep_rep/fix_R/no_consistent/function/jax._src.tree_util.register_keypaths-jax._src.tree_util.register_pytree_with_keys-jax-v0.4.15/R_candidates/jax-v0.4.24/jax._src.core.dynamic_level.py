def dynamic_level() -> int:
  return thread_local_state.trace_state.trace_stack.dynamic.level
