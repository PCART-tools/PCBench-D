@implements(np.sin, module='numpy')
@partial(jit, inline=True)
def sin(x: ArrayLike, /) -> Array:
  return lax.sin(*promote_args_inexact('sin', x))
