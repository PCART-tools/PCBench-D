def record_event_duration_secs(event: str, duration: float):
  """Record an event duration in seconds (float)."""
  for callback in _event_duration_secs_listeners:
    callback(event, duration)
