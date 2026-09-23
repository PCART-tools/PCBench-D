@implements(np.negative, module='numpy')
@partial(jit, inline=True)
def negative(x: ArrayLike, /) -> Array:
  return lax.neg(*promote_args('negative', x))
