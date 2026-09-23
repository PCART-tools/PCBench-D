def _asarray(a):
  # simplified version of jnp.asarray() for local use.
  return a if isinstance(a, ndarray) else api.device_put(a)
