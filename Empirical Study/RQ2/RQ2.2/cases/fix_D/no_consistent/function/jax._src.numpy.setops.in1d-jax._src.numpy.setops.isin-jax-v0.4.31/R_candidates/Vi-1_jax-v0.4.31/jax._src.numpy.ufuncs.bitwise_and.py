@implements(np.bitwise_and, module='numpy')
@partial(jit, inline=True)
def bitwise_and(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.bitwise_and(*promote_args("bitwise_and", x, y))
