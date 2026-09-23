@implements(np.multiply, module='numpy')
@partial(jit, inline=True)
def multiply(x: ArrayLike, y: ArrayLike, /) -> Array:
  x, y = promote_args("multiply", x, y)
  return lax.mul(x, y) if x.dtype != bool else lax.bitwise_and(x, y)
