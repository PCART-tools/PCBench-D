@implements(np.subtract, module='numpy')
@partial(jit, inline=True)
def subtract(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.sub(*promote_args("subtract", x, y))
