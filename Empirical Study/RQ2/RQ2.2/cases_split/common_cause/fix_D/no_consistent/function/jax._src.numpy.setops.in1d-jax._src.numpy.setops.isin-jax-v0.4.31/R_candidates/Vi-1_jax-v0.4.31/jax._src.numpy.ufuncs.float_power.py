@implements(np.float_power, module='numpy')
@partial(jit, inline=True)
def float_power(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.pow(*promote_args_inexact("float_power", x, y))
