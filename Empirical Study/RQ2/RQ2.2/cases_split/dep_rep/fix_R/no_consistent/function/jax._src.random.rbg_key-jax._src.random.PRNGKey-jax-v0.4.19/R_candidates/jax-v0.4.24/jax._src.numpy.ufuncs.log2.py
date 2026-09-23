@implements(np.log2, module='numpy')
@partial(jit, inline=True)
def log2(x: ArrayLike, /) -> Array:
  x, = promote_args_inexact("log2", x)
  return lax.div(lax.log(x), lax.log(_constant_like(x, 2)))
