@implements(np.nextafter, module='numpy')
@partial(jit, inline=True)
def nextafter(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.nextafter(*promote_args_inexact("nextafter", x, y))
