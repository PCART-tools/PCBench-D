@implements(np.equal, module='numpy')
@partial(jit, inline=True)
def equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.eq(*promote_args("equal", x, y))
