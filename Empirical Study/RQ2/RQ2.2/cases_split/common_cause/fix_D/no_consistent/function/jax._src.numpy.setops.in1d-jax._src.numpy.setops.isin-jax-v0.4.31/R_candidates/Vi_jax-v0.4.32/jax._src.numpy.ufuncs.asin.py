@partial(jit, inline=True)
def asin(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arcsin`"""
  return arcsin(*promote_args('asin', x))
