@_wraps(np.isnan, module='numpy')
@jit
def isnan(x):
  _check_arraylike("isnan", x)
  return lax.ne(x, x)
