@_wraps(np.linalg.cholesky)
@jit
def cholesky(a: ArrayLike) -> Array:
  check_arraylike("jnp.linalg.cholesky", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  return lax_linalg.cholesky(a)
