@implements(np.arctan2, module='numpy')
@partial(jit, inline=True)
def arctan2(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.atan2(*promote_args_inexact("arctan2", x, y))
