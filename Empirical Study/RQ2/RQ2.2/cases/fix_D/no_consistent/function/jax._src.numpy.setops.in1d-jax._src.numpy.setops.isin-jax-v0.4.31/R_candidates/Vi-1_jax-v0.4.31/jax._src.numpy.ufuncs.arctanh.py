@implements(np.arctanh, module='numpy')
@partial(jit, inline=True)
def arctanh(x: ArrayLike, /) -> Array:
  return lax.atanh(*promote_args_inexact('arctanh', x))
