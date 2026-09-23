@_wraps(scipy.linalg.tril)
def tril(m, k=0):
  return jnp.tril(m, k)
