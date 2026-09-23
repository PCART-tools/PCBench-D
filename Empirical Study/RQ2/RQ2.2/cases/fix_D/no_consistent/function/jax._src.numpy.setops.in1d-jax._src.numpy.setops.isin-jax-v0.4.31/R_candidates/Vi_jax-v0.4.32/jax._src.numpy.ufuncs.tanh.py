@implements(np.tanh, module='numpy')
@partial(jit, inline=True)
def tanh(x: ArrayLike, /) -> Array:
  return lax.tanh(*promote_args_inexact('tanh', x))
