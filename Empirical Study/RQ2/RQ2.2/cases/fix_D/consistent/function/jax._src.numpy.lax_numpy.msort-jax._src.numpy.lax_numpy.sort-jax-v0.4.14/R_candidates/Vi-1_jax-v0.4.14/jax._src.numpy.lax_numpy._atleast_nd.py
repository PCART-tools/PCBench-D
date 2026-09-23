def _atleast_nd(x: ArrayLike, n: int) -> Array:
  m = ndim(x)
  return lax.broadcast(x, (1,) * (n - m)) if m < n else asarray(x)
