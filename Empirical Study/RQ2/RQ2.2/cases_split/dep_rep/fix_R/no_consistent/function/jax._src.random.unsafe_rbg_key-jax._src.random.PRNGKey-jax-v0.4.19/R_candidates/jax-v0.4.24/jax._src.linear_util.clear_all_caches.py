def clear_all_caches():
  global cache_clearing_funs
  for clear in cache_clearing_funs:
    clear()
