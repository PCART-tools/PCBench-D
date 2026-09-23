def _asarray(a: ArrayLike) -> Array:
  # simplified version of jnp.asarray() for local use.
  return a if isinstance(a, Array) else api.device_put(a)
