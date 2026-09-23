@implements(np.sinh, module='numpy')
@partial(jit, inline=True)
def sinh(x: ArrayLike, /) -> Array:
  return lax.sinh(*promote_args_inexact('sinh', x))
