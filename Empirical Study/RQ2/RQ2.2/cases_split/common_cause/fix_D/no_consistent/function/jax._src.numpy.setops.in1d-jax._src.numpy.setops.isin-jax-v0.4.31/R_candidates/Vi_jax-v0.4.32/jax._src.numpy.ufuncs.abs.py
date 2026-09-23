@partial(jit, inline=True)
def abs(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.absolute`."""
  return absolute(x)
