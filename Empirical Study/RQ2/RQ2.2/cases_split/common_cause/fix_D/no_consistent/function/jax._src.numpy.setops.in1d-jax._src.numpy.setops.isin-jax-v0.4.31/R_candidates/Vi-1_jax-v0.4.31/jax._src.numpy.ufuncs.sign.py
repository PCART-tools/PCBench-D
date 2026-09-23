@implements(np.sign, module='numpy')
@partial(jit, inline=True)
def sign(x: ArrayLike, /) -> Array:
  return lax.sign(*promote_args('sign', x))
