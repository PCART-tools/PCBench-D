def _update_thread_local_jit_state(dynamic):
  # Copies the MainTrace instance, removing any .debug_info or .jaxpr_stack
  # fields that should not be kept alive as part of a cache key.
  # TODO(mattjj): split debug_info and jaxpr_stack out of MainTrace.
  # TODO(mattjj): add a test that verifies that JIT-ted functions are not kept
  # alive by the JIT cache, particularly for nested JIT-ted functions.
  copy = MainTrace(dynamic.level, dynamic.trace_type, **dynamic.payload)
  config.update_thread_local_jit_state(dynamic_trace_state=copy)
