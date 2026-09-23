@implements(np.fabs, module='numpy')
@partial(jit, inline=True)
def fabs(x: ArrayLike, /) -> Array:
  return lax.abs(*promote_args_inexact('fabs', x))
