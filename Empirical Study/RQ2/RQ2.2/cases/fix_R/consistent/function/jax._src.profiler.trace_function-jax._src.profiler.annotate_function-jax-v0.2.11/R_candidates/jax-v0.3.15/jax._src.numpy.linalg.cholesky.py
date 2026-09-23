@_wraps(np.linalg.cholesky)
@jit
def cholesky(a):
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  return lax_linalg.cholesky(a)
