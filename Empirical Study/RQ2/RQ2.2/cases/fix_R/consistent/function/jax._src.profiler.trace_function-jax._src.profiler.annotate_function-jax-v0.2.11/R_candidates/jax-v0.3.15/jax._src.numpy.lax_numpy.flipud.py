@_wraps(np.flipud, lax_description=_ARRAY_VIEW_DOC)
def flipud(m):
  return _flip(m, 0)
