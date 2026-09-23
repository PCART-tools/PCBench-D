@implements(np.maximum, module='numpy')
@partial(jit, inline=True)
def maximum(x: ArrayLike, y: ArrayLike, /) -> Array:
  return lax.max(*promote_args("maximum", x, y))
