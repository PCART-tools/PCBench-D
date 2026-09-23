@partial(partial, tree_map)
def _stop_gradient(x):
  if isinstance(x, core.Tracer):
    return stop_gradient_p.bind(x)
  else:
    return x
