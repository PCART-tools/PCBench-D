def initialize_cache(path):
  """Creates a global cache object.

  Should only be called once per process.

  Will throw an assertion error if called a second time with a different path.

  Args:
    path: path for the cache directory.
  """
  global _cache
  if _cache is not None and _cache._path == pathlib.Path(path):
    logger.warning("Cache already previously initialized at %s", _cache._path)
    return

  assert (
      _cache is None
  ), f"The cache path has already been initialized to {_cache._path}"
  _cache = GFileCache(path)
  logger.warning("Initialized persistent compilation cache at %s", path)
