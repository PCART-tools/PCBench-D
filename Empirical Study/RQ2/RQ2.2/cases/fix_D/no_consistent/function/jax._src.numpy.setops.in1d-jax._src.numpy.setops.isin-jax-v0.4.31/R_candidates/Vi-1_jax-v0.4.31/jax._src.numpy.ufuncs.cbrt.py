@implements(np.cbrt, module='numpy')
@partial(jit, inline=True)
def cbrt(x: ArrayLike, /) -> Array:
  return lax.cbrt(*promote_args_inexact('cbrt', x))
