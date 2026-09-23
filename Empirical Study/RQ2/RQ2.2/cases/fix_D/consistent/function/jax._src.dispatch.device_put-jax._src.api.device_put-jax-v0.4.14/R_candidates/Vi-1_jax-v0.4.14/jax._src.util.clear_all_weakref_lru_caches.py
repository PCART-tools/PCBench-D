def clear_all_weakref_lru_caches():
  for cached_call in _weakref_lru_caches:
    cached_call.cache_clear()
