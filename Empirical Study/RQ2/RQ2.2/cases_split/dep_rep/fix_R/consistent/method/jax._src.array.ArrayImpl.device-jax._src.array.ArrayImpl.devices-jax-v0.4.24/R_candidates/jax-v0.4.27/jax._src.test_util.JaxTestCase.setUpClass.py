  @classmethod
  def setUpClass(cls):
    if TEST_WITH_PERSISTENT_COMPILATION_CACHE.value:
      cls._compilation_cache_exit_stack = ExitStack()
      stack = cls._compilation_cache_exit_stack
      stack.enter_context(config.enable_compilation_cache(True))
      stack.enter_context(config.raise_persistent_cache_errors(True))
      stack.enter_context(config.persistent_cache_min_compile_time_secs(0))
      stack.enter_context(config.persistent_cache_min_entry_size_bytes(0))

      tmp_dir = stack.enter_context(tempfile.TemporaryDirectory())
      compilation_cache.set_cache_dir(tmp_dir)
      stack.callback(lambda: compilation_cache.reset_cache())
