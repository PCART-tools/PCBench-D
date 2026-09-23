@_wraps(np.reciprocal, module='numpy')
@partial(jit, inline=True)
def reciprocal(x: ArrayLike, /) -> Array:
  _check_arraylike("reciprocal", x)
  x, = _promote_dtypes_inexact(x)
  return lax.integer_pow(x, -1)
