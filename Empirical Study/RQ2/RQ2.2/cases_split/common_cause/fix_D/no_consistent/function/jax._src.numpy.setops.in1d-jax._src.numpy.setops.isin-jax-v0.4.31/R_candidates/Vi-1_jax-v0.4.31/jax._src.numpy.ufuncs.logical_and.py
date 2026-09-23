@implements(np.logical_and, module='numpy')
@partial(jit, inline=True)
def logical_and(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.bitwise_and(*map(_to_bool, promote_args("logical_and", x, y)))
