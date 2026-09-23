def set_cache_dir(path) -> None:
  """
  Sets the persistent compilation cache directory.

  After calling this, jit-compiled functions are saved to `path`, so they
  do not need be recompiled if the process is restarted or otherwise run again.
  This also tells Jax where to look for compiled functions before compiling.
  """
  config.config.update("jax_compilation_cache_dir", path)
