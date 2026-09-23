def get_event_listeners() -> list[Callable[[str], None]]:
  """Get event listeners."""
  return list(_event_listeners)
