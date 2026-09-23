def _concatenate(aval, x1, x2):
  return lax.concatenate([x1, x2], 0)
