def get_event_duration_listeners() -> list[Callable[[str, float], None]]:
  """Get event duration listeners."""
  return list(_event_duration_secs_listeners)
