def clear_caches():
  """Clear all compilation and staging caches."""
  # Clear all lu.cache and util.weakref_lru_cache instances (used for staging
  # and Python-dispatch compiled executable caches).
  lu.clear_all_caches()
  util.clear_all_weakref_lru_caches()

  # Clear all C++ compiled executable caches for pjit
  pjit._cpp_pjit_cache.clear()
  xc._xla.PjitFunctionCache.clear_all()

  # Clear all C++ compiled executable caches for pmap
  for fun in _pmap_cache_clears:
    fun._cache_clear()

  # Clear particular util.cache instances.
  dispatch.xla_primitive_callable.cache_clear()
