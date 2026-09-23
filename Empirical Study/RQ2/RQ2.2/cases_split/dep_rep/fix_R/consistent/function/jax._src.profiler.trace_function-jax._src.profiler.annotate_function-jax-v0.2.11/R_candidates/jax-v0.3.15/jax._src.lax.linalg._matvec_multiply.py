@partial(vectorize, signature='(n,m),(m)->(n)')
def _matvec_multiply(a, b):
  return lax.dot(a, b, precision=lax.Precision.HIGHEST)
