def put_executable_and_time(
    cache_key: str,
    module_name: str,
    executable: xla_client.LoadedExecutable,
    backend,
    compile_time: int
) -> None:
  """Adds the 'executable' and its compilation time to the cache repository,
  possibly evicting older entries.
  """
  assert _cache is not None, (
      "initialize_cache must be called before you can call"
      "put_executable_and_time()"
  )
  logger.info(
      "Writing %s to persistent compilation cache with key %s.",
      module_name,
      cache_key,
  )
  serialized_executable = backend.serialize_executable(executable)
  executable_and_time = combine_executable_and_time(
      serialized_executable, compile_time)
  if zstandard:
    compressor = zstandard.ZstdCompressor()
    executable_and_time = compressor.compress(executable_and_time)
  else:
    executable_and_time = zlib.compress(executable_and_time)
  _cache.put(cache_key, executable_and_time)
