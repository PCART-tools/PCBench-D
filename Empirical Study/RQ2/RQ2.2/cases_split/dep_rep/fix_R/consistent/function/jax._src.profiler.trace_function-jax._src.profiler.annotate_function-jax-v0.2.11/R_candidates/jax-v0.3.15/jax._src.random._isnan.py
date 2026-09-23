def _isnan(x):
  return lax.ne(x, x)
