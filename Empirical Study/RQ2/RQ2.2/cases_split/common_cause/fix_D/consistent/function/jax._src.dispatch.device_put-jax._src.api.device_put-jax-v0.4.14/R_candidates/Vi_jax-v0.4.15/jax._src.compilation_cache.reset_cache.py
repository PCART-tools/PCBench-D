def reset_cache():
  global _cache
  assert is_initialized()
  logger.info("Resetting cache at %s.", _cache._path)
  _cache = None
