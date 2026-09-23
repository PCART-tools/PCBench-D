def _cache_write(cache_key: str,
                 compile_time_secs: float,
                 module_name: str,
                 backend: Backend, executable: xc.LoadedExecutable,
                 host_callbacks: list[Any]):
  """Writes the `serialized_computation` and its compilation time to the
  persistent compilation cache repository.
  """
  if host_callbacks:
    logger.info(
        "Not writing persistent cache entry for '%s' because it uses host "
        "callbacks (e.g. from jax.debug.print or breakpoint)", module_name)
    return

  min_compile_time = config.jax_persistent_cache_min_compile_time_secs
  if min_compile_time:
    if compile_time_secs < min_compile_time:
      logger.info(
          "Not writing persistent cache entry for '%s' because it took < %.2f "
          "seconds to compile (%.2fs)", module_name, min_compile_time,
          compile_time_secs)
      return
    else:
      logger.info(
          "'%s' took at least %.2f seconds to compile (%.2fs), writing "
          "persistent cache entry", module_name, min_compile_time,
          compile_time_secs)

  try:
    compilation_cache.put_executable_and_time(
        cache_key, module_name, executable, backend, int(compile_time_secs))
  except Exception as ex:
    if config.jax_raise_persistent_cache_errors:
      raise
    warnings.warn(
        f"Error writing persistent compilation cache entry for "
        f"'{module_name}': {type(ex).__name__}: {ex}")
