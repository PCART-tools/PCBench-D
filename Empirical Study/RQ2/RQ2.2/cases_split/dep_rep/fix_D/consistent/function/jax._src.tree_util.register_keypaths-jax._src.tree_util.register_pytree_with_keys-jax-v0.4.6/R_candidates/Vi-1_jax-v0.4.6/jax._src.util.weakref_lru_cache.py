def weakref_lru_cache(call: Callable, maxsize=2048):
  """
  Least recently used cache decorator with weakref support.

  The cache will take a weakref to the first argument of the wrapped function
  and strong refs to all subsequent operations. In all other respects it should
  behave similar to `functools.lru_cache`.
  """
  return xc.weakref_lru_cache(config._trace_context, call, maxsize)
