def record_event(event: str):
  """Record an event."""
  for callback in _event_listeners:
    callback(event)
