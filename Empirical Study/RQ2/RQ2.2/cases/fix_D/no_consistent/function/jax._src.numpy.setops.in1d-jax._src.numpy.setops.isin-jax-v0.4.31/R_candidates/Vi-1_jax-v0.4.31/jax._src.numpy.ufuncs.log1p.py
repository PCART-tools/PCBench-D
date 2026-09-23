@implements(np.log1p, module='numpy')
@partial(jit, inline=True)
def log1p(x: ArrayLike, /) -> Array:
  return lax.log1p(*promote_args_inexact('log1p', x))
