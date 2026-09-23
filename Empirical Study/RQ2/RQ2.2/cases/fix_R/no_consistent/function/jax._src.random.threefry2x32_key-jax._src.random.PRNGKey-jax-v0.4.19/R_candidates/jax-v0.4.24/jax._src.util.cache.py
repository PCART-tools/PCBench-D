def cache(max_size=4096):
  def wrap(f):
    @functools.lru_cache(max_size)
    def cached(_, *args, **kwargs):
      return f(*args, **kwargs)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
      if config.check_tracer_leaks.value:
        return f(*args, **kwargs)
      else:
        return cached(config.config._trace_context(), *args, **kwargs)

    wrapper.cache_clear = cached.cache_clear
    wrapper.cache_info = cached.cache_info
    return wrapper
  return wrap
