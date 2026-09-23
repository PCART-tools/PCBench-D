@partial(jit, static_argnames=('lower',))
def _cholesky(a, lower):
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  l = lax_linalg.cholesky(a if lower else jnp.conj(_T(a)), symmetrize_input=False)
  return l if lower else jnp.conj(_T(l))
