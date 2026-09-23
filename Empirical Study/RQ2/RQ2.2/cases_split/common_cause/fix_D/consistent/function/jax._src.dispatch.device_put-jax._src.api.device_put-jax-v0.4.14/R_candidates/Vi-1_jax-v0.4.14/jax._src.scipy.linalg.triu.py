@_wraps(scipy.linalg.triu)
def triu(m: ArrayLike, k: int = 0) -> Array:
  return jnp.triu(m, k)
