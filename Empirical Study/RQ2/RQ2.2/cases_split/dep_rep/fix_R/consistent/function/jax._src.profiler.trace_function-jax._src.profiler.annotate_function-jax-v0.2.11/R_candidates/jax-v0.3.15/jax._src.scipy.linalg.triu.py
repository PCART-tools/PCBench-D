@_wraps(scipy.linalg.triu)
def triu(m, k=0):
  return jnp.triu(m, k)
