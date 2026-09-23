@partial(jit, inline=True)
def acos(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arccos`"""
  return arccos(*promote_args('acos', x))
