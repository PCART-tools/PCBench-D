@partial(jit, inline=True)
def acosh(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arccosh`"""
  return arccosh(*promote_args('acosh', x))
