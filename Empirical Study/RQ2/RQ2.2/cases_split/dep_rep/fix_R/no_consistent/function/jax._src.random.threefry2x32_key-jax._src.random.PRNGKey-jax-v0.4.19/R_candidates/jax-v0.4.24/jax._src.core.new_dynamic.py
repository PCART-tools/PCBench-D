@contextmanager
def new_dynamic(level: int) -> Generator[None, None, None]:
  stack = thread_local_state.trace_state.trace_stack
  prev_dynamic, stack.dynamic = stack.dynamic, stack.stack[level]
  _update_thread_local_jit_state(stack.dynamic)
  try:
    yield
  finally:
    stack.dynamic = prev_dynamic
    _update_thread_local_jit_state(stack.dynamic)
