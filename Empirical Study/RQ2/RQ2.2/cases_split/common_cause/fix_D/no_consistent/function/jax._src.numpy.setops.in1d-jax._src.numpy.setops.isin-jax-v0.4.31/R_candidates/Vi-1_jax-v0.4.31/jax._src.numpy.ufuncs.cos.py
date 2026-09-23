@implements(np.cos, module='numpy')
@partial(jit, inline=True)
def cos(x: ArrayLike, /) -> Array:
  return lax.cos(*promote_args_inexact('cos', x))
