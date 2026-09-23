@_wraps(np.square, module='numpy')
@partial(jit, inline=True)
def square(x: ArrayLike, /) -> Array:
  _check_arraylike("square", x)
  x, = _promote_dtypes_numeric(x)
  return lax.integer_pow(x, 2)
