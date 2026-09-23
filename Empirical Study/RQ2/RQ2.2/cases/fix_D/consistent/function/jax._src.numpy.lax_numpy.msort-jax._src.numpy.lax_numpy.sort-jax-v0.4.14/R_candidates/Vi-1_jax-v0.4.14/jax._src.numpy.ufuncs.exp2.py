@_wraps(np.exp2, module='numpy')
@partial(jit, inline=True)
def exp2(x: ArrayLike, /) -> Array:
  x, = promote_args_inexact("exp2", x)
  return lax.exp(lax.mul(lax.log(_constant_like(x, 2)), x))
