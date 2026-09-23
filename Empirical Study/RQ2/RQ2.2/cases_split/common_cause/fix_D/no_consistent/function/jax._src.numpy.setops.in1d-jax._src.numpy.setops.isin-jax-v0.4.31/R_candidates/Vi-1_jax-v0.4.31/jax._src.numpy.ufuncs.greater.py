@implements(np.greater, module='numpy')
@partial(jit, inline=True)
def greater(x: ArrayLike, y: ArrayLike, /) -> Array:
  return _complex_comparison(lax.gt, *promote_args("greater", x, y))
