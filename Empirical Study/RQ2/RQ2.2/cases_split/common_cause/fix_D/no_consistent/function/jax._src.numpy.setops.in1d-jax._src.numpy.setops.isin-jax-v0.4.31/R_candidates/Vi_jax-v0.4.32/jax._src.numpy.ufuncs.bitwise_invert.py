@implements(getattr(np, 'bitwise_invert', np.invert), module='numpy')
@partial(jit, inline=True)
def bitwise_invert(x: ArrayLike, /) -> Array:
  return lax.bitwise_not(*promote_args('bitwise_invert', x))
