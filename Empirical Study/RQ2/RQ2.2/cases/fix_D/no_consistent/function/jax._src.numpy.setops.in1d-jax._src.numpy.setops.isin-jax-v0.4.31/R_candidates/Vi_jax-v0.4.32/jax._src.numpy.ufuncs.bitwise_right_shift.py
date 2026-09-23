@partial(jit, inline=True)
def bitwise_right_shift(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.right_shift`."""
  return right_shift(x1, x2)
