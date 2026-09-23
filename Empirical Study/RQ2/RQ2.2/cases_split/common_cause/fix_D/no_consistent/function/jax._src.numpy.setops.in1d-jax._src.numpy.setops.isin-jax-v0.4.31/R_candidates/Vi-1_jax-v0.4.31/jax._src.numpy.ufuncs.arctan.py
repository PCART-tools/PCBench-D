@implements(np.arctan, module='numpy')
@partial(jit, inline=True)
def arctan(x: ArrayLike, /) -> Array:
  return lax.atan(*promote_args_inexact('arctan', x))
