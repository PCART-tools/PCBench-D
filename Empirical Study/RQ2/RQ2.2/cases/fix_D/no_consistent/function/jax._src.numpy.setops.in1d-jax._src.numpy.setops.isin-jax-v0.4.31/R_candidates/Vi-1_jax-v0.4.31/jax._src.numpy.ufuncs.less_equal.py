@implements(np.less_equal, module='numpy')
@partial(jit, inline=True)
def less_equal(x: ArrayLike, y: ArrayLike, /) -> Array:
  return _complex_comparison(lax.le, *promote_args("less_equal", x, y))
