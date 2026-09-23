@contextlib.contextmanager
def explicit_device_put_scope() -> Iterator[None]:
  """Indicates that the current context is an explicit device_put*() call."""
  state = transfer_guard_lib.thread_local_state()
  prev = state.explicit_device_put
  state.explicit_device_put = True
  try:
    yield
  finally:
    state.explicit_device_put = prev
