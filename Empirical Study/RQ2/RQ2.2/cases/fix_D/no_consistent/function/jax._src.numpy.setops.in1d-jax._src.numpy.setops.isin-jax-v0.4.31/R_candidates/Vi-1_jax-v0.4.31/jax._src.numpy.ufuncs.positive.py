@implements(np.positive, module='numpy')
@partial(jit, inline=True)
def positive(x: ArrayLike, /) -> Array:
  return lax.asarray(*promote_args('positive', x))
