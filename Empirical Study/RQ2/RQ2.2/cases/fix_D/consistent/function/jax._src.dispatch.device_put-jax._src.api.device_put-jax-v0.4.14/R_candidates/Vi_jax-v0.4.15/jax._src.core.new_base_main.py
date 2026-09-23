@contextmanager
def new_base_main(trace_type: type[Trace],
                  **payload) -> Generator[MainTrace, None, None]:
  # See comments in https://github.com/google/jax/pull/3370
  stack = thread_local_state.trace_state.trace_stack
  main = MainTrace(0, trace_type, **payload)
  prev_dynamic, stack.dynamic = stack.dynamic, main
  prev_base, stack.stack[0] = stack.stack[0], main
  _update_thread_local_jit_state(stack.dynamic)
  try:
    yield main
  finally:
    stack.dynamic = prev_dynamic
    stack.stack[0] = prev_base
    _update_thread_local_jit_state(stack.dynamic)

  if config.jax_check_tracer_leaks:
    t = ref(main)
    del main
    if t() is not None:
      leaked_tracers = maybe_find_leaked_tracers(t())
      if leaked_tracers: raise leaked_tracer_error("trace", t(), leaked_tracers)
