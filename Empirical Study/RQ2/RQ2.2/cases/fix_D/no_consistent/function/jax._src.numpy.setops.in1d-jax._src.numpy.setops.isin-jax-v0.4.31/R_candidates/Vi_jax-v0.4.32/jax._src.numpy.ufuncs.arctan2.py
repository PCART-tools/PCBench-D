@implements(np.arctan2, module='numpy')
@partial(jit, inline=True)
def arctan2(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  return lax.atan2(*promote_args_inexact("arctan2", x1, x2))
