@util._wraps(np.fmax, module='numpy')
@jit
def fmax(x1: ArrayLike, x2: ArrayLike) -> Array:
  return where(ufuncs.greater(x1, x2) | ufuncs.isnan(x2), x1, x2)
