def _reshape_staging_rule(
    trace, x, *dyn, new_sizes, dimensions):
  params = dict(new_sizes=new_sizes, dimensions=dimensions)
  if not dyn:
    return trace.default_process_primitive(reshape_p, (x,), params)
  av = core.DShapedArray(_merge_dyn_shape(new_sizes, dyn), x.dtype, x.weak_type)
  return _dyn_shape_staging_rule(trace, reshape_p, av, x, *dyn, **params)
