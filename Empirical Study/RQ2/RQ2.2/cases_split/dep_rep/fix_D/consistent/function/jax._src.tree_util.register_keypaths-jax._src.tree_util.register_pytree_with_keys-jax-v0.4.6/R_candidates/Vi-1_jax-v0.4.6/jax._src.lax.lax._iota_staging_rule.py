def _iota_staging_rule(trace, *dyn_shape, dtype, shape, dimension):
  params = dict(dtype=dtype, shape=shape, dimension=dimension)
  if not dyn_shape:
    return trace.default_process_primitive(iota_p, (), params)
  aval = core.DShapedArray(_merge_dyn_shape(shape, dyn_shape), dtype, False)
  return _dyn_shape_staging_rule(trace, iota_p, aval, *dyn_shape, **params)
