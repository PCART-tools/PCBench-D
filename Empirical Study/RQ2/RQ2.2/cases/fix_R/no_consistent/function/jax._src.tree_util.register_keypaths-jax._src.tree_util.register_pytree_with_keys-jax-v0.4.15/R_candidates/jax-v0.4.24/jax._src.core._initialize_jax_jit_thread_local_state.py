def _initialize_jax_jit_thread_local_state():
  """Initializes the C++ thread-local context.

  When the user spawns threads, the C++ `jax_jit.thread_local_state` is None.
  The C++ accessor calls this function if it realizes the thread_local_state
  is None (which means it's not yet initialized for this thread).

  This function does not live in `config.py`, to prevent circular imports.
  """
  tls = jax_jit.thread_local_state()
  if tls.extra_jit_context is None:
    dynamic = thread_local_state.trace_state.trace_stack.dynamic
    copy = MainTrace(dynamic.level, dynamic.trace_type, **dynamic.payload)
    config.update_thread_local_jit_state(dynamic_trace_state=copy)
