@_wraps(np.fmin, module='numpy')
@jit
def fmin(x1, x2):
  return where((x1 < x2) | isnan(x2), x1, x2)
