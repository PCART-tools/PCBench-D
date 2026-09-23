def initialize_cache(path) -> None:
  """
  This API is deprecated; use set_cache_dir instead.

  Set the path. To take effect, should be called prior to any calls to
  get_executable_and_time() and put_executable_and_time().
  """
  warnings.warn("initialize_cache is deprecated; use set_cache_dir instead",
                DeprecationWarning, stacklevel=2)
  config.config.update("jax_compilation_cache_dir", path)
