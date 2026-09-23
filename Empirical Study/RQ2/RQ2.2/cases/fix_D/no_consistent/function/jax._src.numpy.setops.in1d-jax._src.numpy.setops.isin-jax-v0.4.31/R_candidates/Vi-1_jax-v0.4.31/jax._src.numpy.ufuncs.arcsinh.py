@implements(np.arcsinh, module='numpy')
@partial(jit, inline=True)
def arcsinh(x: ArrayLike, /) -> Array:
  return lax.asinh(*promote_args_inexact('arcsinh', x))
