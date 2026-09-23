@contextmanager
def register_event_duration_listener(callback):
  """Manages registering/unregistering an event duration listener callback."""
  try:
    monitoring.register_event_duration_secs_listener(callback)
    yield
  finally:
    monitoring._unregister_event_duration_listener_by_callback(callback)
