def _combine_leading(sz0, sz1, aval, x):
  assert x.ndim >= 2
  assert x.shape[0] == sz0
  assert x.shape[1] == sz1
  return lax.collapse(x, 0, 2)
