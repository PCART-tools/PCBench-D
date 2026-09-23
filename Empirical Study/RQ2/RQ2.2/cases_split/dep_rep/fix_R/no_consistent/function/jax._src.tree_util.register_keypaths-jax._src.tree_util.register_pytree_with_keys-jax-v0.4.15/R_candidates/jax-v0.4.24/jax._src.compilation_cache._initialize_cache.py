def _initialize_cache() -> None:
  # Attempt to initialize the cache at most once.
  global _cache_initialized
  with _cache_initialized_mutex:
    if _cache_initialized:
      logger.debug("_initialize_cache: cache has already been initialized!")
      return
    _cache_initialized = True

    # Nothing to do if the cache is disabled.
    if not _is_cache_enabled():
      logger.debug("_initialize_cache: cache is disabled!")
      return

    # Set the minimum cache size entry only if the flag
    # --jax_persistent_cache_min_entry_size_bytes has not been set.
    if config.persistent_cache_min_entry_size_bytes.value == 0:
      config.config.update("jax_persistent_cache_min_entry_size_bytes",
                           default_min_cache_entry_size())

    global _cache
    assert _cache is None, "The cache has already been initialized!"
    path: str = config.compilation_cache_dir.value
    # If the path is not set, the cache will not be enabled.
    if not path:
      return

    _cache = get_file_cache(path)
    logger.debug("Initialized persistent compilation cache at %s", path)
