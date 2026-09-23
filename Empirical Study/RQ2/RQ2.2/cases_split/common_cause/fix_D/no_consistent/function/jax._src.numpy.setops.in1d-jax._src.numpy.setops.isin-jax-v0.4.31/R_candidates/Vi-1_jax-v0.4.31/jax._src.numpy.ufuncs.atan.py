@partial(jit, inline=True)
def atan(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arctan`"""
  return arctan(*promote_args('atan', x))
