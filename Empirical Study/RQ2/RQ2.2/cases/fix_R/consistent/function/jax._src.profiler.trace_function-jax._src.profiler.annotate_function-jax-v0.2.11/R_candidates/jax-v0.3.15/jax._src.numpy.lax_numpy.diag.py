@_wraps(np.diag, lax_description=_ARRAY_VIEW_DOC)
def diag(v, k=0):
  return _diag(v, operator.index(k))
