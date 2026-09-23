def _empty_array(sz, aval):
  return lax.broadcast(lax.empty(aval.dtype), (sz, *aval.shape))
