def put_executable_and_time(
    cache_key: str,
    module_name: str,
    executable: xla_client.LoadedExecutable,
    backend,
    compile_time: int
) -> None:
  """Adds the 'executable' and its compilation time to the cache, possibly
  evicting older entries.
  """
  cache = _get_cache()
  if cache is None:
    logger.debug("put_executable_and_time: cache is disabled/not initialized")
    return

  serialized_executable = backend.serialize_executable(executable)
  executable_and_time = combine_executable_and_time(
      serialized_executable, compile_time)
  executable_and_time = compress_executable(executable_and_time)

  min_entry_size = config.persistent_cache_min_entry_size_bytes.value
  entry_size = len(executable_and_time)
  if entry_size < min_entry_size:
    logger.info(
        "Not writing cache entry with key %s since its size (%d bytes) "
        "is less than threshold (%d bytes)",
        cache_key,
        entry_size,
        min_entry_size,
    )
  else:
    logger.debug(
        "Writing %s to persistent compilation cache with key %s.",
        module_name,
        cache_key
    )
    monitoring.record_event('/jax/compilation_cache/cache_misses')
    cache.put(cache_key, executable_and_time)
