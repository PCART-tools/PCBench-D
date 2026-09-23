@_wraps(np.fmax, module='numpy')
@jit
def fmax(x1, x2):
  return where((x1 > x2) | isnan(x2), x1, x2)
