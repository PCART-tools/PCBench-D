@implements(np.expm1, module='numpy')
@partial(jit, inline=True)
def expm1(x: ArrayLike, /) -> Array:
  return lax.expm1(*promote_args_inexact('expm1', x))
