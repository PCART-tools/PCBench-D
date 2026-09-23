@implements(np.log, module='numpy')
@partial(jit, inline=True)
def log(x: ArrayLike, /) -> Array:
  return lax.log(*promote_args_inexact('log', x))
