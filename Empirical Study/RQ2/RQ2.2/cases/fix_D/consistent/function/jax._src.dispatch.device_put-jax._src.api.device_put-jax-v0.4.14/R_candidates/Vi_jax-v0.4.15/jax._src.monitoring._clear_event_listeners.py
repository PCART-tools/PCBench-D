def _clear_event_listeners():
  """Clear event listeners."""
  global _event_listeners, _event_duration_secs_listeners
  _event_listeners = []
  _event_duration_secs_listeners = []
