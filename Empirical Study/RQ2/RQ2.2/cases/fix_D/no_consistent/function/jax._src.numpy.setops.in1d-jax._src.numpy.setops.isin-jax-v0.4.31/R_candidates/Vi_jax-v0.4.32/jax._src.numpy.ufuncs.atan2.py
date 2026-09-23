@partial(jit, inline=True)
def atan2(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arctan2`"""
  return arctan2(*promote_args('atan2', x1, x2))
