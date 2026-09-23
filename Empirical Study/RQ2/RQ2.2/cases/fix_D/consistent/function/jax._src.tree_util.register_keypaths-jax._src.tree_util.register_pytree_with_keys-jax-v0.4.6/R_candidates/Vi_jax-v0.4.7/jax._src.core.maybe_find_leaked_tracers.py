def maybe_find_leaked_tracers(x: Optional[Union[MainTrace, Sublevel]]
                              ) -> List[Tracer]:
  """Find the leaked tracers holding a reference to the MainTrace or SubLevel.

  It's possible there's none! eg. there's some cases where JAX itself holds a
  reference to `x` inside of a lambda closure, and no tracers were leaked
  by the user. In this case an empty list is returned.
  """
  if not getattr(threading.current_thread(), 'pydev_do_not_trace', True):
    warnings.warn(TRACER_LEAK_DEBUGGER_WARNING)
  # Trigger garbage collection to filter out unreachable objects that are alive
  # only due to cyclical dependencies. (We don't care about unreachable leaked
  # tracers since they can't interact with user code and cause a problem.)
  gc.collect()
  traces = list(filter(lambda x: isinstance(x, Trace), gc.get_referrers(x)))
  tracers = list(filter(lambda x: isinstance(x, Tracer), gc.get_referrers(*traces)))
  return tracers
