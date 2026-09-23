def record_event(event: str) -> None:
  """Record an event."""
  for callback in _event_listeners:
    callback(event)
