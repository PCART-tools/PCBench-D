@implements(np.logical_xor, module='numpy')
@partial(jit, inline=True)
def logical_xor(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.bitwise_xor(*map(_to_bool, promote_args("logical_xor", x, y)))
