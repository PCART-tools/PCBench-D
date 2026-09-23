@partial(vectorize, signature='(n,m),(m)->(n)')
def _matvec_multiply(a: Array, b: Array) -> Array:
  return lax.dot(a, b, precision=lax.Precision.HIGHEST)
