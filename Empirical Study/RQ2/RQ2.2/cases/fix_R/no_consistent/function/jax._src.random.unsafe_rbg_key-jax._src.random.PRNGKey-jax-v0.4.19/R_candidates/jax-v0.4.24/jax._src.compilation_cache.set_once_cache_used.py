def set_once_cache_used(f) -> None:
  """One-time setting of _cache_used.

  If _cache_used is False, set it to True and execute the provided function
  f. No action if _cache_used is True. This provides a mechanism to execute f
  once per task. Note that reset_cache() will reset _cache_used also.
  """
  global _cache_used
  with _cache_initialized_mutex:
    if not _cache_used:
      _cache_used = True
      if f is not None:
        f()
