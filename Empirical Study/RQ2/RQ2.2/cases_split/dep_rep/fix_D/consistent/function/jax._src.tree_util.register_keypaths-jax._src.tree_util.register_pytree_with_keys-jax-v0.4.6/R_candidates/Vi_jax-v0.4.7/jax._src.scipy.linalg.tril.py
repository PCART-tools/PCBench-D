@_wraps(scipy.linalg.tril)
def tril(m: ArrayLike, k: int = 0) -> Array:
  return jnp.tril(m, k)
