@_wraps(np.fliplr, lax_description=_ARRAY_VIEW_DOC)
def fliplr(m):
  return _flip(m, 1)
