@implements(np.sqrt, module='numpy')
@partial(jit, inline=True)
def sqrt(x: ArrayLike, /) -> Array:
  return lax.sqrt(*promote_args_inexact('sqrt', x))
