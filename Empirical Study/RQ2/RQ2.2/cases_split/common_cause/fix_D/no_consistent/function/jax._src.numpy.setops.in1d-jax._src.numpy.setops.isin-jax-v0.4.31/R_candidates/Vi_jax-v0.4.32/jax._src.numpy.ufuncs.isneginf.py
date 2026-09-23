@implements(np.isposinf, module='numpy')
def isneginf(x, /, out=None):
  return _isposneginf(-np.inf, x, out)
