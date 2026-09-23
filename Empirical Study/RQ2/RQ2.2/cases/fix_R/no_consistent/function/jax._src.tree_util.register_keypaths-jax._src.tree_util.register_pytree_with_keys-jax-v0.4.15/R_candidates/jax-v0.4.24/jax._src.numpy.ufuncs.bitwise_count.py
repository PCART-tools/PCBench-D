@implements(getattr(np, 'bitwise_count', None), module='numpy')
@jit
def bitwise_count(x: ArrayLike, /) -> Array:
  x, = promote_args_numeric("bitwise_count", x)
  # Following numpy we take the absolute value and return uint8.
  return lax.population_count(abs(x)).astype('uint8')
