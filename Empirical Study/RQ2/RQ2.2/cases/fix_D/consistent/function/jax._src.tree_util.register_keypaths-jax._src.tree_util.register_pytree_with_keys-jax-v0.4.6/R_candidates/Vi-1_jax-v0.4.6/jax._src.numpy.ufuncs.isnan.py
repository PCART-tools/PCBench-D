@_wraps(np.isnan, module='numpy')
@jit
def isnan(x: ArrayLike, /) -> Array:
  _check_arraylike("isnan", x)
  return lax.ne(x, x)
