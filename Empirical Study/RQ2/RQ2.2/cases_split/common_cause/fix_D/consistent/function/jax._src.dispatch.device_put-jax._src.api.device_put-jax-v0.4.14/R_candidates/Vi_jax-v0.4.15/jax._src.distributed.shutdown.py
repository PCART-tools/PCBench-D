def shutdown():
  """Shuts down the distributed system.

  Does nothing if the distributed system is not running."""
  global_state.shutdown()
