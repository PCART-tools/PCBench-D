def _prepend_dim_to_aval(sz, aval):
  return core.unmapped_aval(sz, core.no_axis_name, 0, aval)
