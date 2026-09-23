@_wraps(np.log10, module='numpy')
@partial(jit, inline=True)
def log10(x: ArrayLike, /) -> Array:
  x, = promote_args_inexact("log10", x)
  return lax.div(lax.log(x), lax.log(_constant_like(x, 10)))
