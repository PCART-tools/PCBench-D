@implements(np.cosh, module='numpy')
@partial(jit, inline=True)
def cosh(x: ArrayLike, /) -> Array:
  return lax.cosh(*promote_args_inexact('cosh', x))
