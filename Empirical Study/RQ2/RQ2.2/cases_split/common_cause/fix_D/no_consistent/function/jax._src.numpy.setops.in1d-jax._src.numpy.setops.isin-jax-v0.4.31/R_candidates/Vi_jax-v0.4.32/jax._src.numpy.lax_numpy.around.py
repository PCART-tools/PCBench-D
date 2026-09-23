@partial(jit, static_argnames=('decimals',))
def around(a: ArrayLike, decimals: int = 0, out: None = None) -> Array:
  """Alias of :func:`jax.numpy.round`"""
  return round(a, decimals, out)
