@implements(np.greater_equal, module='numpy')
@partial(jit, inline=True)
def greater_equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  return _complex_comparison(lax.ge, *promote_args("greater_equal", x, y))
