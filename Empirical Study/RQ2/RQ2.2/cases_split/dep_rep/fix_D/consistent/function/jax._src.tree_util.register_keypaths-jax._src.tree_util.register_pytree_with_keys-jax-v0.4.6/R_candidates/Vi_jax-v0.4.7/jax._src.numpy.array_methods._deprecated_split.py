@util._wraps(lax.broadcast, lax_description="""
Deprecated. Use :func:`jax.numpy.split` instead.
""")
def _deprecated_split(*args, **kwargs):
  warnings.warn(
    "The arr.split() method is deprecated. Use jax.numpy.split instead.",
    category=FutureWarning)
  return lax_numpy.split(*args, **kwargs)
