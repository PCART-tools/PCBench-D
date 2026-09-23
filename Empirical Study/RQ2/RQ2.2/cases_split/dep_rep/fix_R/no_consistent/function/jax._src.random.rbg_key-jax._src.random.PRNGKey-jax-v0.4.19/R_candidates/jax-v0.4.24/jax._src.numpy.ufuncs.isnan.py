@implements(np.isnan, module='numpy')
@partial(jit, inline=True)
def isnan(x: ArrayLike, /) -> Array:
  check_arraylike("isnan", x)
  return lax.ne(x, x)
