def disable_all_debug_logging():
  """Disables all debug logging enabled via `enable_debug_logging`.

  The default logging behavior will still be in effect, i.e. WARNING and above
  will be logged to stderr without extra message formatting.
  """
  for logger in _debug_enabled_loggers:
    logger.removeHandler(_debug_handler)
    # Assume that the default non-debug log level is always WARNING. In theory
    # we could keep track of what it was set to before. This shouldn't make a
    # difference if not other handlers are attached, but set it back in case
    # something else gets attached (e.g. absl logger) and for consistency.
    logger.setLevel(logging.WARNING)
