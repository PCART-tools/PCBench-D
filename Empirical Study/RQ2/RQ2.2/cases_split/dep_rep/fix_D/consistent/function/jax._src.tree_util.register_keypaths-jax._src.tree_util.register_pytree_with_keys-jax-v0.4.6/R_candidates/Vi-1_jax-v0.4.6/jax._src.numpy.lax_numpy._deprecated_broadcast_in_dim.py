@util._wraps(lax.broadcast, lax_description="""
Deprecated. Use :func:`jax.lax.broadcast_in_dim` instead.
""")
def _deprecated_broadcast_in_dim(*args, **kwargs):
  warnings.warn(
    "The arr.broadcast_in_dim() method is deprecated. Use jax.lax.broadcast_in_dim instead.",
    category=FutureWarning)
  return lax.broadcast_in_dim(*args, **kwargs)
