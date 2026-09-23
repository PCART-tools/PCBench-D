@implements(np.true_divide, module='numpy')
@partial(jit, inline=True)
def true_divide(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  x1, x2 = promote_args_inexact("true_divide", x1, x2)
  return lax.div(x1, x2)
