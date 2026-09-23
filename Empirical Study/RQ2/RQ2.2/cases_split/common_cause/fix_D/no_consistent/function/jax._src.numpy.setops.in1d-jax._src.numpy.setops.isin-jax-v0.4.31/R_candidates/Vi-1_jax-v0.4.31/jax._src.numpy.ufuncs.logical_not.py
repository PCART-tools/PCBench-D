@implements(np.logical_not, module='numpy')
@partial(jit, inline=True)
def logical_not(x: ArrayLike, /) -> Array:
  return lax.bitwise_not(*map(_to_bool, promote_args("logical_not", x)))
