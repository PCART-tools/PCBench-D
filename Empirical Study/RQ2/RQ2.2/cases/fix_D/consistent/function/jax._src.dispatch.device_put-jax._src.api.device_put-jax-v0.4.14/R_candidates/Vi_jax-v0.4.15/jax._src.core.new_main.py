@contextmanager
def new_main(trace_type: type[Trace],
             dynamic: bool = False,
             **payload) -> Generator[MainTrace, None, None]:
  # See comments in https://github.com/google/jax/pull/3370
  stack = thread_local_state.trace_state.trace_stack
  level = stack.next_level()
  main = MainTrace(level, trace_type, **payload)
  stack.push(main)
  if dynamic:
    prev_dynamic, stack.dynamic = stack.dynamic, main
    _update_thread_local_jit_state(stack.dynamic)

  try:
    yield main
  finally:
    stack.pop()
    if dynamic:
      stack.dynamic = prev_dynamic
      _update_thread_local_jit_state(stack.dynamic)

  if config.jax_check_tracer_leaks:
    t = ref(main)
    del main
    if t() is not None:
      leaked_tracers = maybe_find_leaked_tracers(t())
      if leaked_tracers: raise leaked_tracer_error("trace", t(), leaked_tracers)
