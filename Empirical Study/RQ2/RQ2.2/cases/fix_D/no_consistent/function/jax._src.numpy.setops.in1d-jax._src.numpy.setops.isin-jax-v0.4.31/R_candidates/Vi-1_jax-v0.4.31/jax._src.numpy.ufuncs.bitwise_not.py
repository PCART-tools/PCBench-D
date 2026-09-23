@implements(np.bitwise_not, module='numpy')
@partial(jit, inline=True)
def bitwise_not(x: ArrayLike, /) -> Array:
  return lax.bitwise_not(*promote_args('bitwise_not', x))
