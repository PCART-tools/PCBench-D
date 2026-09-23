def _broadcast_in_dim_staging_rule(
    trace, x, *dyn, shape, broadcast_dimensions):
  params = dict(shape=shape, broadcast_dimensions=broadcast_dimensions)
  if not dyn:
    return trace.default_process_primitive(broadcast_in_dim_p, (x,), params)
  aval = core.DShapedArray(_merge_dyn_shape(shape, dyn), x.dtype, x.weak_type)
  return _dyn_shape_staging_rule(trace, broadcast_in_dim_p, aval, x, *dyn,
                                 **params)
