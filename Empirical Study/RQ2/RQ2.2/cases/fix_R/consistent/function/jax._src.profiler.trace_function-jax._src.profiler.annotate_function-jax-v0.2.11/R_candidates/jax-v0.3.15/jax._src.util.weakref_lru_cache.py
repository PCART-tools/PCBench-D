def weakref_lru_cache(call: Callable, maxsize=2048):
  """
  Least recently used cache decorator with weakref support.

  The cache will take a weakref to the first argument of the wrapped function
  and strong refs to all subsequent operations. In all other respects it should
  behave similar to `functools.lru_cache`.
  """
  cache: Dict[Any, Any] = {}
  hits = misses = 0
  lock = threading.Lock()

  def remove_key(tctx, args, kwargs, weak_arg):
    k = (weak_arg, tctx, args, kwargs)
    try:
      # This has a chance to race with the iteration in next(iter(cache)),
      # but we cannot lock because GC can get triggered synchronously inside
      # a critical section and will not relinquish control until the callback
      # has finished. This would lead to a deadlock between this weakref
      # cleanup function and any function below which locks.
      del cache[k]
    except KeyError:
      pass

  def wrapped(weak_arg, *args, **kwargs):
    nonlocal hits, misses
    if config.jax_check_tracer_leaks:
      return call(weak_arg, *args, **kwargs)
    kwargs_key = tuple(kwargs.items())
    tctx = config._trace_context()
    k = (weakref.ref(weak_arg,
         functools.partial(remove_key, tctx, args, kwargs_key)),
         tctx, args, kwargs_key)
    with lock:
      if k in cache:
        hits += 1
        result = cache[k]
        # del and reinsert to bump key in the insertion order.
        del cache[k]
        cache[k] = result
        return result
      misses += 1
    result = call(weak_arg, *args, **kwargs)
    with lock:
      cache[k] = result
      num_errors = 0
      while len(cache) > maxsize:
        try:
          del_k = next(iter(cache))
          # This happens if a weakref callback happens between iter and
          # next. Just ignore the error. WeakKeyDictionary handles this
          # by deferring the deletes, but that has a chance at leaking,
          # and this solution is easier.
        except RuntimeError:
          num_errors += 1
          if num_errors > len(cache):
            # This must be some other problem.
            raise
          else:
            continue
        del cache[del_k]
      return result

  def cache_info():
    with lock:
      return CacheInfo(hits, misses, maxsize, len(cache))

  def cache_clear():
    nonlocal hits, misses
    with lock:
      hits = misses = 0
      cache.clear()

  wrapped.cache_info = cache_info
  wrapped.cache_clear = cache_clear
  return wrapped
