def _unregister_event_duration_listener_by_callback(
    callback: EventDurationListenerWithMetadata) -> None:
  """Unregister an event duration listener by callback.

  This function is supposed to be called for testing only.
  """
  assert callback in _event_duration_secs_listeners
  _event_duration_secs_listeners.remove(callback)
