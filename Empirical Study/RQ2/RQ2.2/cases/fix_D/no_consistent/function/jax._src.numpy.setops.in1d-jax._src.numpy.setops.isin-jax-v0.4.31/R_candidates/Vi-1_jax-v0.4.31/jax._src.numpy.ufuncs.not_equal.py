@implements(np.not_equal, module='numpy')
@partial(jit, inline=True)
def not_equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.ne(*promote_args("not_equal", x, y))
