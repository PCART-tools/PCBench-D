@implements(np.isposinf, module='numpy')
def isposinf(x, /, out=None):
  return _isposneginf(np.inf, x, out)
