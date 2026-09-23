def _cache_write(serialized_computation: Union[str, bytes, ir.Module],
                 compile_time_secs: float,
                 module_name: str, compile_options: CompileOptions,
                 backend: Backend, compiled: xc.LoadedExecutable,
                 host_callbacks: List[Any]):
  """Writes `serialized_computation` to the persistent compilation cache."""
  # Avoid import cycle between jax and jax.experimental
  from jax.experimental.compilation_cache import compilation_cache as cc

  if host_callbacks:
    logger.info(
        "Not writing persistent cache entry for '%s' because it uses host "
        "callbacks (e.g. from jax.debug.print or breakpoint)")
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
    cc.put_executable(module_name, serialized_computation, compile_options,
                      compiled, backend)
  except Exception as ex:
    if config.jax_raise_persistent_cache_errors:
      raise
    warnings.warn(
        f"Error writing persistent compilation cache entry for "
        f"'{module_name}': {type(ex).__name__}: {ex}")
