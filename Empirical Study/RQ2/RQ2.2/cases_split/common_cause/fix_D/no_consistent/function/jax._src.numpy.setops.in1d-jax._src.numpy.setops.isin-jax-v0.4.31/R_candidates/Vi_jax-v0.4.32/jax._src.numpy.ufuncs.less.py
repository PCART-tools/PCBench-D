@implements(np.less, module='numpy')
@partial(jit, inline=True)
def less(x: ArrayLike, y: ArrayLike, /) -> Array:
  return _complex_comparison(lax.lt, *promote_args("less", x, y))
