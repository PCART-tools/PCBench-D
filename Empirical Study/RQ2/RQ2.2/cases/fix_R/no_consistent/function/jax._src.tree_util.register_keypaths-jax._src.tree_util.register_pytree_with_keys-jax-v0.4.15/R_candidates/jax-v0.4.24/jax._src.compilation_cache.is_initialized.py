def is_initialized() -> bool:
  """
  Deprecated.

  Return whether the cache is enabled. Initialization can be deferred, so
  initialized status is not checked. The name is retained for backwards
  compatibility.
  """
  warnings.warn("is_initialized is deprecated; do not use",
                DeprecationWarning, stacklevel=2)
  return _is_cache_enabled()
