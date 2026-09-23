@_wraps(np.reciprocal, module='numpy')
@partial(jit, inline=True)
def reciprocal(x: ArrayLike, /) -> Array:
  check_arraylike("reciprocal", x)
  x, = promote_dtypes_inexact(x)
  return lax.integer_pow(x, -1)
