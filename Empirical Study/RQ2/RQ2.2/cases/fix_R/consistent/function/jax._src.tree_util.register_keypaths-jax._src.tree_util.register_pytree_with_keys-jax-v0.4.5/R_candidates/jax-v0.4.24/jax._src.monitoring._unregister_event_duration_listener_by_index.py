def _unregister_event_duration_listener_by_index(index: int) -> None:
  """Unregister an event duration listener by index.

  This function is supposed to be called for testing only.
  """
  size = len(_event_duration_secs_listeners)
  assert -size <= index < size
  del _event_duration_secs_listeners[index]
