@implements(np.arcsin, module='numpy')
@partial(jit, inline=True)
def arcsin(x: ArrayLike, /) -> Array:
  return lax.asin(*promote_args_inexact('arcsin', x))
