def _cache_read(
    module_name: str, cache_key: str, compile_options: xc.CompileOptions,
    backend: xc.Client
) -> tuple[xc.LoadedExecutable | None, int | None]:
  """Looks up the `computation` and it's compilation time in the persistent
  compilation cache repository.
  """
  try:
    return compilation_cache.get_executable_and_time(
        cache_key, compile_options, backend)
  except Exception as ex:
    if config.raise_persistent_cache_errors.value:
      raise
    warnings.warn(
        f"Error reading persistent compilation cache entry for "
        f"'{module_name}': {type(ex).__name__}: {ex}")
    return None, None
