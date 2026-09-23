def _unregister_event_listener_by_callback(
    callback: EventListenerWithMetadata) -> None:
  """Unregister an event listener by callback.

  This function is supposed to be called for testing only.
  """
  assert callback in _event_listeners
  _event_listeners.remove(callback)
