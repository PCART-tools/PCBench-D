@implements(np.arccos, module='numpy')
@partial(jit, inline=True)
def arccos(x: ArrayLike, /) -> Array:
  return lax.acos(*promote_args_inexact('arccos', x))
