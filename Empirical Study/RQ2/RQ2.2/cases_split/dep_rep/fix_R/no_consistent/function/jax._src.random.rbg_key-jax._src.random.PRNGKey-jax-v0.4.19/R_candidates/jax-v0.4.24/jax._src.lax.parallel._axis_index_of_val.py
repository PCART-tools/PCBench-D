def _axis_index_of_val(x, val, axis_name):
  idx = axis_index(axis_name)
  validx = lax_numpy.where(val == x, idx, dtypes.iinfo(dtypes.dtype(idx)).max)
  return pmin(validx, axis_name)
