@implements(np.bitwise_or, module='numpy')
@partial(jit, inline=True)
def bitwise_or(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.bitwise_or(*promote_args("bitwise_or", x, y))
