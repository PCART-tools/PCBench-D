@implements(np.linalg.cholesky)
@partial(jit, static_argnames=['upper'])
def cholesky(a: ArrayLike, *, upper: bool = False) -> Array:
  check_arraylike("jnp.linalg.cholesky", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  if upper:
    a = jax.numpy.matrix_transpose(a).conj()
  return lax_linalg.cholesky(a)
