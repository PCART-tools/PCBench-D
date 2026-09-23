@_wraps(np.exp2, module='numpy')
@partial(jit, inline=True)
def exp2(x: ArrayLike, /) -> Array:
  x, = promote_args_inexact("exp2", x)
  return lax.exp2(x)
