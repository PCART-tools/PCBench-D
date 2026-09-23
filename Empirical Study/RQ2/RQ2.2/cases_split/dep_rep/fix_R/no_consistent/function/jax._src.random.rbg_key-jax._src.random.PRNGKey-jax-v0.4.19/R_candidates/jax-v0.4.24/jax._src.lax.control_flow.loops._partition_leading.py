def _partition_leading(sz0, sz1, aval, x):
  assert x.ndim >= 1
  assert x.shape[0] == sz0 * sz1
  return lax.reshape(x, (sz0, sz1, *x.shape[1:]))
