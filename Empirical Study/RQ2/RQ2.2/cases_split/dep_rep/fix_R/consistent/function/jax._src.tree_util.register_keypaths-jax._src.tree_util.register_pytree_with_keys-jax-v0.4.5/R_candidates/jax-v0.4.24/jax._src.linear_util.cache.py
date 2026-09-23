def cache(call: Callable, *, explain: Callable | None = None):
  """Memoization decorator for functions taking a WrappedFun as first argument.

  Args:
    call: a Python callable that takes a WrappedFun as its first argument. The
      underlying transforms and params on the WrappedFun are used as part of the
      memoization cache key.

  Returns:
     A memoized version of ``call``.
  """
  fun_caches: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

  def memoized_fun(fun: WrappedFun, *args):
    cache = fun_caches.setdefault(fun.f, new_cache := {})  # type: ignore
    if config.check_tracer_leaks.value:
      key = (_copy_main_traces(fun.transforms), fun.params, fun.in_type, args,
             config.enable_x64.value, config.default_device.value,
             config.config._trace_context())
    else:
      key = (fun.transforms, fun.params, fun.in_type, args, config.enable_x64.value,
             config.default_device.value, config.config._trace_context())
    result = cache.get(key, None)
    if result is not None:
      ans, stores = result
      fun.populate_stores(stores)
    else:
      ans = call(fun, *args)
      if explain and config.explain_cache_misses.value:
        explain(fun.f, cache is new_cache, cache, key, ans)
      cache[key] = (ans, fun.stores)

    return ans

  def _evict_function(f):
    fun_caches.pop(f, None)

  memoized_fun.cache_clear = fun_caches.clear  # type: ignore
  memoized_fun.evict_function = _evict_function  # type: ignore

  cache_clearing_funs.add(memoized_fun.cache_clear)

  return memoized_fun
