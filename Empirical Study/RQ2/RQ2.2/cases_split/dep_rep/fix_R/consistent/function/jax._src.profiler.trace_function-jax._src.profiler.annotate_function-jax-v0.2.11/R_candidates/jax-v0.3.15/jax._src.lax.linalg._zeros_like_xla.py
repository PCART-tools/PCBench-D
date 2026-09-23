def _zeros_like_xla(c, aval):
  zero = xops.Constant(c, np.array(0, aval.dtype))
  return xops.Broadcast(zero, aval.shape)
