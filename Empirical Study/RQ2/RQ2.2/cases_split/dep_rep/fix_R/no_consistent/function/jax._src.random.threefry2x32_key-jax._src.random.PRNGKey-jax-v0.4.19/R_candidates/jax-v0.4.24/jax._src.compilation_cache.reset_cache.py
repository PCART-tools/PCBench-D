def reset_cache() -> None:
  """Get back to pristine, uninitialized state."""
  global _cache
  global _cache_initialized
  global _cache_used
  logger.debug("Resetting cache at %s.",
               _cache._path if _cache is not None else "<empty>")
  _cache = None
  with _cache_initialized_mutex:
    _cache_initialized = False
    _cache_used = False
