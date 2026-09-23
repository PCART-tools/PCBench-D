@implements(np.invert, module='numpy')
@partial(jit, inline=True)
def invert(x: ArrayLike, /) -> Array:
  return lax.bitwise_not(*promote_args('invert', x))
