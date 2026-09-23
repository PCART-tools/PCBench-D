def get_executable_and_time(
    cache_key: str, compile_options, backend
) -> tuple[Optional[xla_client.LoadedExecutable], Optional[int]]:
  """Returns the cached executable and its compilation time if present, or None
  otherwise.
  """
  assert _cache is not None, (
      "initialize_cache must be called before you can call"
      " get_executable_and_time()"
  )
  executable_and_time = _cache.get(cache_key)
  if not executable_and_time:
    return None, None
  if zstandard:
    decompressor = zstandard.ZstdDecompressor()
    executable_and_time = decompressor.decompress(executable_and_time)
  else:
    executable_and_time = zlib.decompress(executable_and_time)
  serialized_executable, compile_time = extract_executable_and_time(
      executable_and_time)
  xla_executable_deserialized = backend.deserialize_executable(
      serialized_executable, compile_options)
  return xla_executable_deserialized, compile_time
