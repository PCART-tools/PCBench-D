@_wraps(np.hypot, module='numpy')
@jit
def hypot(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  _check_arraylike("hypot", x1, x2)
  x1, x2 = _promote_dtypes_inexact(x1, x2)
  x1 = lax.abs(x1)
  x2 = lax.abs(x2)
  x1, x2 = maximum(x1, x2), minimum(x1, x2)
  return lax.select(x1 == 0, x1, x1 * lax.sqrt(1 + lax.square(lax.div(x2, lax.select(x1 == 0, lax._ones(x1), x1)))))
