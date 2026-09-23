@implements(np.exp, module='numpy')
@partial(jit, inline=True)
def exp(x: ArrayLike, /) -> Array:
  return lax.exp(*promote_args_inexact('exp', x))
