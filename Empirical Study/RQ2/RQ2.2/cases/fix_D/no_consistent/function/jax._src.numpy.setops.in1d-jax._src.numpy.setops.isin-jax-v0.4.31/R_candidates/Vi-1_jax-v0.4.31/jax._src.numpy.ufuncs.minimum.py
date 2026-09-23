@implements(np.minimum, module='numpy')
@partial(jit, inline=True)
def minimum(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.min(*promote_args("minimum", x, y))
