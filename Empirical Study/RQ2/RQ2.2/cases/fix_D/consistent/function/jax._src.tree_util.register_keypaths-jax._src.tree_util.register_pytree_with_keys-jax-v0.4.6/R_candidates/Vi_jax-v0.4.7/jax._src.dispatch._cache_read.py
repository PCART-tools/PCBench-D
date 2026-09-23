def _cache_read(computation: Union[str, bytes, ir.Module], module_name: str,
                compile_options: CompileOptions,
                backend: Backend) -> Optional[xc.LoadedExecutable]:
  """Looks up `computation` in the persistent compilation cache."""
  # Avoid import cycle between jax and jax.experimental
  from jax.experimental.compilation_cache import compilation_cache as cc

  try:
    return cc.get_executable(computation, compile_options, backend)
  except Exception as ex:
    if config.jax_raise_persistent_cache_errors:
      raise
    warnings.warn(
        f"Error reading persistent compilation cache entry for "
        f"'{module_name}': {type(ex).__name__}: {ex}")
    return None
