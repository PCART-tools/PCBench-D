@partial(partial, tree_map)
def _copy_main_traces(x):
  if isinstance(x, core.MainTrace):
    return core.MainTrace(x.level, x.trace_type, **x.payload)
  else:
    return x
