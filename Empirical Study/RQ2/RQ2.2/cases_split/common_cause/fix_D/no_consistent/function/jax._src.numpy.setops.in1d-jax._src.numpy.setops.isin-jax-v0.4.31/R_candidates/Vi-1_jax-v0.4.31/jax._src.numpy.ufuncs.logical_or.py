@implements(np.logical_or, module='numpy')
@partial(jit, inline=True)
def logical_or(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.bitwise_or(*map(_to_bool, promote_args("logical_or", x, y)))
