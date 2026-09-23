def _empty_array(sz, aval):
  return lax.full((sz,) + aval.shape, 0, aval.dtype)
