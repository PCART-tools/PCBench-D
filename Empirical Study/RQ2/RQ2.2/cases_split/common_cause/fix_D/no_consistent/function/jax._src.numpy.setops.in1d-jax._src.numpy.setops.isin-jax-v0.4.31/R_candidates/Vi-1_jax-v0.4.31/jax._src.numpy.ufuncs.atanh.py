@partial(jit, inline=True)
def atanh(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arctanh`"""
  return arctanh(*promote_args('atanh', x))
