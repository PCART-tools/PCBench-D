@implements(np.tan, module='numpy')
@partial(jit, inline=True)
def tan(x: ArrayLike, /) -> Array:
  return lax.tan(*promote_args_inexact('tan', x))
