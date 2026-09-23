@implements(np.bitwise_xor, module='numpy')
@partial(jit, inline=True)
def bitwise_xor(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.bitwise_xor(*promote_args("bitwise_xor", x, y))
