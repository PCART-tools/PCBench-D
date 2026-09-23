def cache(call: Callable):
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
    cache = fun_caches.setdefault(fun.f, {})
    if config.jax_check_tracer_leaks:
      key = (_copy_main_traces(fun.transforms), fun.params, fun.in_type, args,
             config.x64_enabled, config.jax_default_device,
             config._trace_context())
    else:
      key = (fun.transforms, fun.params, fun.in_type, args, config.x64_enabled,
             config.jax_default_device, config._trace_context())
    result = cache.get(key, None)
    if result is not None:
      ans, stores = result
      fun.populate_stores(stores)
    else:
      ans = call(fun, *args)
      cache[key] = (ans, fun.stores)

    return ans

  def _evict_function(f):
    fun_caches.pop(f, None)

  memoized_fun.cache_clear = fun_caches.clear  # type: ignore
  memoized_fun.evict_function = _evict_function  # type: ignore

  return memoized_fun
