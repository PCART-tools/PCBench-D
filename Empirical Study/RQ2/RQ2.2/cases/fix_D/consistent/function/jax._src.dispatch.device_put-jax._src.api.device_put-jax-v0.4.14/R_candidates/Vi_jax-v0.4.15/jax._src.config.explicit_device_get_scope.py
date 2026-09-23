@contextlib.contextmanager
def explicit_device_get_scope() -> Iterator[None]:
  """Indicates that the current context is an explicit device_get() call."""
  state = transfer_guard_lib.thread_local_state()
  prev = state.explicit_device_get
  state.explicit_device_get = True
  try:
    yield
  finally:
    state.explicit_device_get = prev
