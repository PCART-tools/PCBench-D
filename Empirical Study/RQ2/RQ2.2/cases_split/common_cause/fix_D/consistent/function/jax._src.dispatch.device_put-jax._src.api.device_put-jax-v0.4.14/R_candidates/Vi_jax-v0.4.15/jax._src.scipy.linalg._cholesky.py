@partial(jit, static_argnames=('lower',))
def _cholesky(a: ArrayLike, lower: bool) -> Array:
  a, = promote_dtypes_inexact(jnp.asarray(a))
  l = lax_linalg.cholesky(a if lower else jnp.conj(a.mT), symmetrize_input=False)
  return l if lower else jnp.conj(l.mT)
