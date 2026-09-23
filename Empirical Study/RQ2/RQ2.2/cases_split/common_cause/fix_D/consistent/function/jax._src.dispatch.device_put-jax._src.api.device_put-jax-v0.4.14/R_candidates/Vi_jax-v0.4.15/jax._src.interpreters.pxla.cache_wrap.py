def cache_wrap(fn):
  _wrapped_with_lu_cache = lu.cache(fn)
  _wrapped_with_weakref_lru_cache = weakref_lru_cache(fn)
  def wrapped(f, *args, **kwargs):
    if isinstance(f, lu.WrappedFun):
      return _wrapped_with_lu_cache(f, *args, **kwargs)
    else:
      return _wrapped_with_weakref_lru_cache(f, *args, **kwargs)
  return wrapped
