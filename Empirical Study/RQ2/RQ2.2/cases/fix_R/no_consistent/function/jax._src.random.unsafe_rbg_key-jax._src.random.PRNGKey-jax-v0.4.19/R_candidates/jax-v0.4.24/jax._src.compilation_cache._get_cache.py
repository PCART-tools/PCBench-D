def _get_cache() -> CacheInterface | None:
  # TODO(b/289098047): consider making this an API and changing the callers of
  # get_executable_and_time() and put_executable_and_time() to call get_cache()
  # and passing the result to them.
  if _cache is None:
    _initialize_cache()  # initialization is done at most once; see above
  return _cache
