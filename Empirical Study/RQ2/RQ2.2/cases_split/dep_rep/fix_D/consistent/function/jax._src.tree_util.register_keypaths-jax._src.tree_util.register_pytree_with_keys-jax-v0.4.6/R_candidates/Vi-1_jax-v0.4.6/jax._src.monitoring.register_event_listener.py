def register_event_listener(callback: Callable[[str], None]):
  """Register a callback to be invoked during record_event()."""
  _event_listeners.append(callback)
