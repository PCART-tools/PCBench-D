@partial(jit, inline=True)
def asinh(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arcsinh`"""
  return arcsinh(*promote_args('asinh', x))
