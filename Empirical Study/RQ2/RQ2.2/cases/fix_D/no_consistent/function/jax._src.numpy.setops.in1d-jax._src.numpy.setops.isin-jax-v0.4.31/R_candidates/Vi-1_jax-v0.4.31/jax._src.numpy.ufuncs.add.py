@implements(np.add, module='numpy')
@partial(jit, inline=True)
def add(x: ArrayLike, y: ArrayLike, /) -> Array:
  x, y = promote_args("add", x, y)
  return lax.add(x, y) if x.dtype != bool else lax.bitwise_or(x, y)
