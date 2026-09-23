@util.implements(np.fmin, module='numpy')
@jit
def fmin(x1: ArrayLike, x2: ArrayLike) -> Array:
  return where(ufuncs.less(x1, x2) | ufuncs.isnan(x2), x1, x2)
