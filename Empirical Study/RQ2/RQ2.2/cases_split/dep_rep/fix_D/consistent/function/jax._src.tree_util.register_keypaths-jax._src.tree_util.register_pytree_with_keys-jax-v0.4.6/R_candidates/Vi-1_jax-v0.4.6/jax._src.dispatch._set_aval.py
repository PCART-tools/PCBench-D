def _set_aval(val):
  if val.aval is None:
    val.aval = core.ShapedArray(val.shape, val.dtype)
  return val
