@partial(jit, static_argnames=('full_matrices', 'compute_uv'))
def _svd(a, *, full_matrices, compute_uv):
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  return lax_linalg.svd(a, full_matrices=full_matrices, compute_uv=compute_uv)
