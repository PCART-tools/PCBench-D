@util._wraps(lax.broadcast, lax_description="""
Deprecated. Use :func:`jax.lax.broadcast` instead.
""")
def _deprecated_broadcast(*args, **kwargs):
  warnings.warn(
    "The arr.broadcast() method is deprecated. Use jax.lax.broadcast instead.",
    category=FutureWarning)
  return lax.broadcast(*args, **kwargs)
