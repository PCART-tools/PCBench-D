  @classmethod
  def tearDownClass(cls):
    if TEST_WITH_PERSISTENT_COMPILATION_CACHE.value:
      cls._compilation_cache_exit_stack.close()
